import csv
import re

from itemadapter import ItemAdapter
from sqlalchemy import create_engine, Engine
from scrapy.exceptions import NotSupported
from sqlalchemy.orm import sessionmaker

from model import CompanyRatingModel


def validate_correct_keys(item: dict, require_fields: list):
    missing_keys = [key for key in require_fields if key not in item]
    return missing_keys


def validate_fields(method):
    def wrapper(pipeline, item: dict, *args):
        require_fields = pipeline.__class__.require_fields
        missing_key = validate_correct_keys(item, require_fields)
        if missing_key:
            raise NotSupported(f"The wrong key was passed: {missing_key}")
        if len(item.keys()) != len(require_fields):
            raise NotSupported(
                f"The required number of keys was not transmitted: {len(item.keys())}, expected:{len(require_fields)}")

        return method(pipeline, item, *args)

    return wrapper


class BasePipeline:
    require_fields = ['name', 'city', 'country', 'status']

    @validate_fields
    def process_item(self, item, spider):
        item['name'] = item['name'].strip()
        item['city'] = self.process_city(item['city'])
        item['country'] = item['country'].replace(" ", "")
        item['status'] = self.process_status(item['status'])
        return item

    @staticmethod
    def process_city(data):
        if not data:
            return None

        data_list = [d.strip() for d in data.split(",")]
        try:
            city = data_list[4]
            if city == "-":
                city = data_list[3] if data_list[3] != "-" else data_list[2]
        except IndexError:
            city = data

        filtered_city = re.sub(r'(\.|г \.|Г \.|г. \.|Г. \.|Г\.|г\.|д\.|п\.|рп\.|с\.|ст-ца|село|пос\.|город\s)', '',
                               city).strip()
        return filtered_city

    @staticmethod
    def process_status(status):

        if "Исключено" in status:
            return 5
        elif "Действительно":
            return 0
        elif not status:
            raise NotSupported("The status field can't be empty")
        else:
            raise NotSupported(f"Status field cannot be resolved and converted: {status}")


class NoprizPipeline(BasePipeline):

    def __init__(self):
        super().__init__()
        self.require_fields += ["email"]

    @validate_fields
    def process_item(self, item, spider):
        item = super().process_item(item, spider)
        item["email"] = self.process_email(item["email"])
        return item

    @staticmethod
    def process_email(email):
        if not email:
            return None
            # raise NotSupported(f"The mail field can't be empty")
        elif "@" in email:
            return email
        return None
        # raise NotSupported(f"Incorrect mail format: {email}")


class ProcurementPipeline(BasePipeline):

    @validate_fields
    def process_item(self, item, spider):
        item = super().process_item(item, spider)
        return item


class EgrzPipeline(BasePipeline):
    @validate_fields
    def process_item(self, item, spider):
        item = super().process_item(item, spider)
        return item




# -- Не используются ---

class CSVPipeline:
    def __init__(self, csv_filename):
        self.csv_filename = csv_filename

    def create_model(self, item):
        return {
            'name': item['name'],
            'city': item['city'],
            'country': item['country'],
            'status': item['status'],
            'email': item['email']
        }

    def add_model(self, model):
        with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'city', 'country', 'status', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Если файл пустой, добавляем заголовки
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow(model)

    def process_item(self, item, spider):
        model = self.create_model(item)
        self.add_model(model)

        return item


class PostgreSQLSingleton:
    _instance = None

    def __new__(cls) -> Engine:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = create_engine('postgresql://{}:{}@{}/{}'.format(*cls.__get_db_config()))
            cls._instance.Session = sessionmaker(bind=cls._instance.engine)
        return cls._instance

    @staticmethod
    def __get_db_config():
        import configparser
        config = configparser.ConfigParser()
        config.read("parser_bot\site_rating_scraper\scrapy.cfg")
        return (config['database']['user'], config['database']['password'],
                config['database']['host'], config['database']['name'])

    def close(self):
        self.engine.dispose()


class PostrgreSQLPipeline:
    @staticmethod
    def create_model(item):
        model_instance = CompanyRatingModel(
            name=item['name'],
            city=item['city'],
            country=item['country'],
            status=item['status'],
            email=item['email']
        )
        return model_instance

    @staticmethod
    def add_model(model, session):
        try:
            session.add(model)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def process_item(self, item, spider):
        db = PostgreSQLSingleton()
        session = db.Session()

        model = self.create_model(item)
        self.add_model(model, session)

        return item

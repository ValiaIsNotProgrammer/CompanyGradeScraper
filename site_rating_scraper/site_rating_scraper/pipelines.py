import re

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SiteRatingScraperPipeline:
    def process_item(self, item, spider):
        item['number'] = item['number'].strip()
        item['tin'] = item['tin'].replace(" ", "")
        item['city'] = self.process_city(item['city'])
        return item

    @staticmethod
    def process_city(data):
        if not data:
            return None

        data_list = [d.strip() for d in data.split(",")]
        city = data_list[4]
        if city == "-":
            city = data_list[3] if data_list[3] != "-" else data_list[2]

        filtered_city = re.sub(r'(\.|г \.|Г \.|г. \.|Г. \.|Г\.|г\.|д\.|п\.|рп\.|с\.|ст-ца|село|пос\.|город\s)', '', city).strip()
        return filtered_city

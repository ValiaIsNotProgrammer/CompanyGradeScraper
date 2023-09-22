from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class CompanyRatingModel(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    country = Column(String)
    status = Column(Integer)
    email = Column(String)

    def __init__(self, name, city, country, status, email):
        self.name = name
        self.city = city
        self.country = country
        self.status = status
        self.email = email
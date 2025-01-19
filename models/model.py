from sqlalchemy import Column, BigInteger, DateTime, Integer, Text, func, Boolean, Float
from sqlalchemy.orm import declarative_base


Base = declarative_base() 

class TravelAgency(Base):
    __tablename__ = 'travel_agency'

    id = Column(BigInteger, primary_key=True, nullable=False)
    country_name = Column(Text)
    independent = Column(Text)
    un_member = Column(Text)
    start_of_week = Column(Text)
    official_country_name = Column(Text)
    common_native_name = Column(Text)
    idd_root = Column(Text)
    idd_suffixes =  Column(Text)
    capital = Column(Text)
    region = Column(Text)
    sub_region = Column(Text)
    languages = Column(Text)
    area = Column(Float) 
    population = Column(Integer)
    continents = Column(Text)
    currencies = Column(Text)
    currency_code = Column(Text)

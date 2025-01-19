from sqlalchemy import create_engine
from decouple import config
from sqlalchemy.orm import sessionmaker, scoped_session

user = config("USER")
host = config("HOST")
password = config("PASSWORD")
database = config("DATABASE")
db_url = f"postgresql+psycopg2://{user}:{password}@{host}/{database}"

def get_db() -> scoped_session:
    """ Connect to Postgres"""
    engine = create_engine(db_url, pool_size=1, max_overflow=1)
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    TennisSession = scoped_session(session)
    return TennisSession


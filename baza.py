from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine(
    f'sqlite:///parkovka_sber.db'
)

local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

db = local_session()

Base = declarative_base()

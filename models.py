import sqlalchemy
from sqlalchemy import create_engine, Integer, String, Column, BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine('sqlite:///data.db?check_same_thread=False')


class Formula(Base):
    __tablename__ = 'formulas'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    schema = Column(BLOB)
    formula = Column(BLOB)
    text_formula = Column(String)


Base.metadata.create_all(engine)
Session = sessionmaker(engine)
session = Session()

# session.close()

from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Column,Integer,String,DateTime,create_engine
from sqlalchemy import ForeignKey
from datetime import datetime

#connection
connection_string = 'postgresql+psycopg2://username:password@postgres-service:5432/database'
engine = create_engine(connection_string,echo=True)
Base=declarative_base()

# table scraping
class scraping(Base):
    __tablename__ = 'scraping'
    id = Column(Integer(),primary_key=True)
    product = Column(String(100),nullable=True)
    price = Column(String(25),nullable=True)
    createdtime = Column(DateTime(),default=datetime.utcnow)
    __table_args__ = {'schema': 'landing'}

# table brand dimension table
class brand_dim(Base):
    __tablename__ = 'brand_dim'
    id = Column(Integer(),primary_key=True)
    brand = Column(String(100),nullable=False,unique=True)
    createdtime = Column(DateTime(),default=datetime.utcnow)
    children = relationship("transaction_fact")
    __table_args__ = {'schema': 'dw'}


class transaction_fact(Base):
   __tablename__ = 'transaction_fact'
   id = Column(Integer(),primary_key=True)
   product = Column(String(100),nullable=False)
   brand_id = Column(Integer(),ForeignKey('dw.brand_dim.id'),nullable=True)
   price = Column(Integer())
   createdtime = Column(DateTime(),default=datetime.utcnow)
   __table_args__ = {'schema': 'dw'}

if __name__ == '__main__' :

    #create schema
    engine.execute('''CREATE SCHEMA IF NOT EXISTS landing''')

    #create schema
    engine.execute('''CREATE SCHEMA IF NOT EXISTS dw''')
    
    Base.metadata.create_all(engine)


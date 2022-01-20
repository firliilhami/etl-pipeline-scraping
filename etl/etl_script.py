import pandas as pd
import numpy as np

from sqlalchemy.dialects.postgresql import insert

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,func
from sqlalchemy.dialects.postgresql import insert

from main import scraping,transaction_fact,brand_dim



# extract data from landing
def extract(last_etl):
    if last_etl == None :
        data = local_session.query(scraping)
        df = pd.read_sql(data.statement,local_session.bind)
    else :
        data = local_session.query(scraping).filter(scraping.createdtime > last_etl)
        df = pd.read_sql(data.statement,local_session.bind)

    print(f"Last ETL : {last_etl}")
    
    return df


def transform(df):
    df = df.copy()
    # cleansing price
    df['price'] = df['price'].str.lower()
    df['price'] = df['price'].str.replace('.','',regex=True)
    df['price'] = df['price'].str.replace('rp','',regex=True)
    df['price'] = df['price'].astype('int32')

    # create column brand
    list_brand = ['acer','lenovo','asus','macbook']
    df['product'] = df['product'].str.lower()
    df['brand'] = 'None'
    for brand in list_brand :
        df['brand'] = np.where(df['product'].str.contains(brand),brand,df['brand'])
    
    return df

def load_brand_dim(df):
    df = df.copy()
    list_brand = df[df['brand']!='None']['brand'].unique().tolist()
    for brand in list_brand:
        statement = insert(brand_dim).values(brand=brand).on_conflict_do_nothing(index_elements=['brand'])
        local_session.execute(statement)
        local_session.commit()
    print('dw.brand_dim table is updated')

def load_transaction_fact(df):
    df = df.copy()
    brand_table = local_session.query(brand_dim.id.label("brand_id"),brand_dim.brand)
    brand_table = pd.read_sql(brand_table.statement,local_session.bind)

    df = pd.merge(df,brand_table,how='left',on='brand')
    df = df.replace({np.nan:None})

    for product,brand_id,price in df[['product','brand_id','price']].to_numpy():
        new_data = transaction_fact(product=product,brand_id=brand_id,price=price)
        local_session.add(new_data)
        local_session.commit()
    print('dw.transaction_fact is updated')

if __name__ == '__main__':
    # connection
    connection_string = 'postgresql+psycopg2://username:password@postgres-service:5432/database'
    engine = create_engine(connection_string,echo=False)
    # make local session to access database
    Session = sessionmaker()
    local_session = Session(bind=engine)

    # get last_etl time
    last_etl = local_session.query(func.max(transaction_fact.createdtime)).first()[0]
    df = extract(last_etl)
    df = transform(df)
    load_brand_dim(df)
    load_transaction_fact(df)
    print("Finish")
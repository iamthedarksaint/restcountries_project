import pandas as pd   
import requests
from datetime import datetime
import random
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.db import get_db
from models.model import TravelAgency


def load():
    url = "https://restcountries.com/v3.1/all?fields=name,independent,unMember,startOfWeek,currencies,idd,capital,region,subregion,languages,area,population,continents"

    response = requests.get(url)
    print(f"Converting data to Json...")
    data = response.json()
    return data

def transform(data=dict) -> pd.DataFrame:
    all_columns = []
    for column in data:
        all_columns.append([column.get('name').get('common'),
                        column.get('independent'),
                        column.get('unMember'),
                        column.get('startOfWeek'),
                        column.get('name').get('official'),
                        [val.get('common') for val in column.get('name', {}).get('nativeName', {}).values()],
                        column.get('currencies').keys(),
                        [val.get('name') for val in column.get('currencies', {}).values()],
                        [val.get('symbol') for val in column.get('currencies', {}).values()],
                        column.get('idd').get('root'),
                        column.get('idd').get('suffixes'),
                        column.get('capital'),
                        column.get('region'),
                        column.get('subregion'),
                        column.get('languages').values(),
                        column.get('area'),
                        column.get('population'),
                        column.get('continents')
                        ]
                       )

    df = pd.DataFrame(all_columns)
    df.columns = ['country_name', 'independent','un_member', 'start_of_week','official_country_name','common_native_name','currency_code', 'currency_name', 'currency_symbol', 'idd_root', 'idd_suffixes', 'capital', 'region', 'sub_region', 'languages', 'area', 'population', 'continents']
    df['currency_code'] = df['currency_code'].apply(list)
    df['languages'] = df['languages'].apply(list)
    return df

def store(df=pd.DataFrame):
    print('storing data......')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    df.to_csv(f"datalake/restcountries_{timestamp}.csv")
    print(f"Data saved as csv file.")

def update(df:pd.DataFrame):
    travel_db = get_db()
    db_data = [
        TravelAgency(
            id = random.randint(1000,1000000),
            country_name = row['country_name'],
            independent = row['independent'],
            un_member = row['un_member'],
            start_of_week = row['start_of_week'],
            official_country_name =  row['official_country_name'],
            common_native_name = row['common_native_name'],
            idd_root = row['idd_root'],
            idd_suffixes = row['idd_suffixes'],
            capital = row['capital'],
            region = row['region'],
            sub_region = row['sub_region'],
            languages = row['languages'],
            area = row['area'],
            population = row['population'],
            continents = row['continents'],
            currency_code = row['currency_code'],
            currency_name = row['currency_name'],
            currency_symbol = row['currency_symbol']
    )
    for row in df.to_dict(orient='records')
    ]
    travel_db.add_all(db_data)
    travel_db.commit()
    print("Database updated successfully.") 


def main():
    data = load()
    clean_data = transform(data)
    # store(clean_data)
    update(clean_data)


if __name__ == '__main__':
    main()
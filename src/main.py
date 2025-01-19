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
    data = response.json()
    print(f"Converting data to DataFrame...")
    df = pd.json_normalize(data)
    return df

def transform(df=pd.DataFrame) -> pd.DataFrame:
    print('transforming data......')
    language = [col for col in df.columns if col.startswith('languages.')]

    currencies = [col for col in df.columns if col.startswith('currencies.')]

    df['languages'] = df[language].apply(lambda x: ", ".join(x.dropna()), axis=1)

    df['currencies'] = df[currencies].apply(lambda x: ", ".join(x.dropna()), axis=1)

    df = df[['name.common', 'independent', 'unMember', 'startOfWeek', 'name.official', 'name.nativeName.eng.common', 'idd.root', 'idd.suffixes', 'capital', 'region', 'subregion', 'languages', 'area', 'population', 'continents', 'currencies', 'currency_code']]

    df = df.rename(columns={'name.common': 'country_name','unMember':'un_member','startOfWeek': 'start_of_week', 'name.official':'official_country_name', 'name.nativeName.eng.common': 'common_native_name', 'idd.root': 'idd_root', 'idd.suffixes': 'idd_suffixes', 'subregion':'sub_region'})
    print("Data has been cleaned!")
    return df

def store(df=pd.DataFrame):
    print('storing data......')
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') 
    df.to_parquet(f"datalake/restcountries_{timestamp}.parquet")
    print(f"Data saved as parquet file.")
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
            currencies = row['currencies'],
            currency_code = row['currency_code']
    )
    for row in df.to_dict(orient='records')
    ]
    travel_db.add_all(db_data)
    travel_db.commit()
    print("Database updated successfully.") 


def main():
    data = load()
    clean_data = transform(data)
    store(clean_data)
    update(clean_data)


if __name__ == '__main__':
    main()
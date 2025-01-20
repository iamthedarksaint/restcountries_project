import requests
import pandas as pd

url = "https://restcountries.com/v3.1/all?fields=name,independent,unMember,startOfWeek,currencies,idd,capital,region,subregion,languages,area,population,continents"

response = requests.get(url)
data = response.json()
print(f"Converting data to DataFrame...")
# df = pd.json_normalize(data)
# return df

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
df.columns = ['country_name', 'independent','unmember', 'start_of_week','official_country_name','common_native_name','currency_code', 'currency_name', 'currency_symbol', 'idd_root', 'idd_suffixes', 'capital', 'region', 'sub_region', 'langauges', 'area', 'population', 'continents']
print(df.head())

print(df.dtypes)

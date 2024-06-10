import requests
import sqlite3
import pandas as pd
from pandas import json_normalize
from sqlalchemy import create_engine
import schedule
import time

def collect_security_incidents(api_url):
    response = requests.get(api_url)
    data = response.json()
    incidents_df = json_normalize(data['results'][0])  # Assuming the API returns a list with a single dictionary
    return incidents_df

def store_data(df, db_name, table_name):
    engine = create_engine(f'sqlite:///{db_name}.db')
    df.to_sql(table_name, engine, if_exists='replace', index=False)

def update_data():
    api_url = "https://randomuser.me/api/"
    new_data = collect_security_incidents(api_url)
    store_data(new_data, 'security_data', 'incidents')
    print("Data updated.")

# Schedule the update every 10 seconds
schedule.every(1).minute.do(update_data)

while True:
    schedule.run_pending()
    time.sleep(1)


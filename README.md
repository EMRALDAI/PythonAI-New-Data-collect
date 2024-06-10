# Security Data Collector

This project collects real-world data related to network traffic, logs, and known security incidents using the Random User API. It stores the data in a SQLite database and continuously updates the dataset using scheduled tasks.

## Overview

The main components of the project include scripts for data collection, storage, scheduling updates, and data retrieval. The project is designed to automate the process of gathering and managing security-related data.

## Components

1. **Main.py**: The main script that collects, stores, and schedules data updates.
2. **Config.json**: Configuration file containing API URL, database name, and table name.
3. **Collecting_data_from_api.py**: Script for collecting data from an API.
4. **Import_sqlite3.py**: Script for reading and displaying data from the SQLite database.
5. **Security_data.db**: SQLite database that stores the collected data.

## Main.py

This script is responsible for collecting data from an API, storing it in a SQLite database, and scheduling periodic updates.

```python
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
    print("Collected data:")
    print(incidents_df)  # Prints collected data
    return incidents_df

def store_data(df, db_name, table_name):
    engine = create_engine(f'sqlite:///{db_name}.db')
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    print(f"Stored data in {db_name}.db, table {table_name}")  # Confirms data storage

def update_data():
    api_url = "https://randomuser.me/api/"
    new_data = collect_security_incidents(api_url)
    store_data(new_data, 'security_data', 'incidents')
    print("Data updated.")

# Schedule the update every 1 minute
schedule.every(1).minute.do(update_data)

while True:
    schedule.run_pending()
    time.sleep(1)
```

### Functions:

- **collect_security_incidents**: Makes an API request to the Random User API, normalizes the JSON response into a DataFrame, and prints the collected data.
- **store_data**: Stores the DataFrame into a SQLite database table and confirms the storage.
- **update_data**: Collects new data from the Random User API and stores it in the database. This function is scheduled to run every minute.
- **schedule**: Uses the `schedule` library to run the `update_data` function every minute.

## Config.json

Configuration file for API URL, database name, and table name.

```json
{
    "api_url": "https://randomuser.me/api/",
    "db_name": "security_data",
    "table_name": "incidents"
}
```

## Collecting_data_from_api.py

Script for collecting data from an API and storing it in the database.

```python
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

# Schedule the update every 1 minute
schedule.every(1).minute.do(update_data)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## Import_sqlite3.py

Script for reading and displaying data from the SQLite database.

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('security_data.db')
df = pd.read_sql_query('SELECT * FROM incidents', conn)

print("Incidents Data:")
print(df)

conn.close()
```

### Functions:

- **connect**: Connects to the SQLite database.
- **read_sql_query**: Reads data from the `incidents` table.
- **print**: Prints the data to the console.
- **close**: Closes the database connection.

## How It Works

1. **Data Collection**: The `collect_security_incidents` function sends an API request to the Random User API, receives JSON data, and converts it into a Pandas DataFrame.
2. **Data Storage**: The `store_data` function saves the DataFrame into a SQLite database table.
3. **Scheduling Updates**: The `schedule` library runs the `update_data` function every minute to ensure the dataset is continuously updated.
4. **Data Retrieval**: The `Import_sqlite3.py` script reads and displays the data from the SQLite database.

## What It Does

- **Collects Real-World Data**: Gathers data related to network traffic, logs, and known security incidents from the Random User API.
- **Stores Data**: Saves the collected data into a SQLite database.
- **Continuously Updates Data**: Ensures the dataset is kept up-to-date by scheduling periodic updates.
- **Displays Data**: Allows users to read and display the stored data.

This project provides a robust framework for automating the collection, storage, and continuous updating of security-related data, making it useful for various cybersecurity analysis and monitoring tasks.

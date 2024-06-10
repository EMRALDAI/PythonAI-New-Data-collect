import sqlite3
import pandas as pd

conn = sqlite3.connect('security_data.db')
df = pd.read_sql_query('SELECT * FROM incidents', conn)

print("Incidents Data:")
print(df)

conn.close()
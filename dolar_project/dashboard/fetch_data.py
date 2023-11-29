from datetime import datetime, date
from prophet import Prophet
from propeht.serialize import model_to_json
import pandas as pd
import requests
import psycopg2
import os

HOST = os.getenv('POSTGRES_HOST', 'None')
PORT = os.getenv('POSTGRES_PORT', 'None')
USER = os.getenv('POSTGRES_USER', 'None')
PASSWORD = os.getenv('POSTGRES_PASSWORD', 'None')
DB = os.getenv('POSTGRES_DB', 'None')

def train_prophet(data: pd.DataFrame) -> None:
    model = Prophet()
    model.fit(data)
    with open('serialized_model.json', 'w') as model_archive:
        model_archive.write(model_to_json(model))

def train_models(data: list) -> None:
    df_prophet = pd.DataFrame(data, columns =['ds', 'y'])
    train_prophet(df_prophet)

def fetch_data_from_api(table):
    conn_string = f"host='{HOST}' port='{PORT}' dbname='{DB}' user='{USER}' password='{PASSWORD}'"
    conn = psycopg2.connect(conn_string)
    db_cursor = conn.cursor()

    db_cursor.execute("SELECT * FROM dashboard_dolarprice ORDER BY date_registered DESC LIMIT 1")
    last_registry_date = db_cursor.fetchone()[1]
    today = date.today()

    outdated_days = abs((last_registry_date-today).days)

    r = requests.get(f'https://economia.awesomeapi.com.br/json/daily/USD-BRL/{outdated_days*3}')

    list_dolar = []

    for data in r.json():
        list_dolar.append({'date': datetime.fromtimestamp(int(data['timestamp'])).date(), 'value': float(data['bid'])})

    df = pd.DataFrame(list_dolar)

    df = df.drop_duplicates(subset='date', keep='first').reset_index(drop=True)

    datas_completas = pd.date_range(start=df['date'].iloc[-1], end=today, freq='D')

    df_completo = pd.DataFrame({'date': datas_completas})

    df['date'] = pd.to_datetime(df['date'])

    df_correct = df_completo.merge(df, on='date', how='left')

    df_correct['value'] = df_correct['value'].fillna(method='ffill')

    df_correct['date'] = pd.to_datetime(df_correct['date'])

    reference = pd.to_datetime(last_registry_date)

    df_filtered = df_correct[df_correct['date'] > reference].reset_index(drop=True)

    df_filtered.apply(lambda row: db_cursor.execute(
            f"INSERT INTO {table} (date_registered, price) VALUES (%s, %s)",
            (row['date'], row['value'])
        ), axis=1)

    conn.commit()

    if outdated_days > 0:
        train_data_query = f"SELECT date_registered, price FROM dashboard_dolarprice ORDER BY date_registered DESC LIMIT {365*5}"
        db_cursor.execute(train_data_query)
        query_result = db_cursor.fetchall()
        train_models(query_result)

    db_cursor.close()
    conn.close()
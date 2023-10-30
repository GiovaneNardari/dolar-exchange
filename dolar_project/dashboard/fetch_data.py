from datetime import datetime, date
import pandas as pd
import requests

def fetch_data_from_api(conn, table):
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
        ), axis = 1)
    
    conn.commit()
    db_cursor.close()
    conn.close()
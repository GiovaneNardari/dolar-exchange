from prophet import Prophet
from propeht.serialize import model_from_json
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import os

HOST = os.getenv('POSTGRES_HOST', 'None')
PORT = os.getenv('POSTGRES_PORT', 'None')
USER = os.getenv('POSTGRES_USER', 'None')
PASSWORD = os.getenv('POSTGRES_PASSWORD', 'None')
DB = os.getenv('POSTGRES_DB', 'None')

def predict_from_model():
    with open('serialized_model.json', 'r') as model_archive:
        model = model_from_json(model_archive.read())

    future = model.make_future_dataframe(periods=14)
    forecast = model.predict(future)
    forecast = forecast.tail(14)

    conn_string = f"host='{HOST}' port='{PORT}' dbname='{DB}' user='{USER}' password='{PASSWORD}'"
    conn = psycopg2.connect(conn_string)
    db_cursor = conn.cursor()
    db_cursor.execute("SELECT date_registered, price FROM dashboard_dolarprice ORDER BY date_registered DESC LIMIT 60")
    data = db_cursor.fetchall()
    
    df_true = pd.DataFrame(data, columns=["ds", "y"])

    plt.plot(forecast[["ds", "y"]])
    plt.plot(df_true)
    plot_image_path = "static/images/plot01.png"
    plt.savefig(plot_image_path)

    return forecast, plot_image_path
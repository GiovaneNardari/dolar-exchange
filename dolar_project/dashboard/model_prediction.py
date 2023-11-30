from statsmodels.iolib.smpickle import load_pickle
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
    model = load_pickle('serialized_model.pickle')

    conn_string = f"host='{HOST}' port='{PORT}' dbname='{DB}' user='{USER}' password='{PASSWORD}'"
    conn = psycopg2.connect(conn_string)
    db_cursor = conn.cursor()
    db_cursor.execute("SELECT date_registered, price FROM dashboard_dolarprice ORDER BY date_registered DESC LIMIT 60")
    data = db_cursor.fetchall()
    
    df_true = pd.DataFrame(data, columns=['date_registered', 'price'])
    forecast = model.forecast(14)
    
    plt.plot(df_true)
    plt.plot(forecast)
    plot_image_path = "static/images/plot01.png"
    plt.savefig(plot_image_path)

    return forecast, plot_image_path
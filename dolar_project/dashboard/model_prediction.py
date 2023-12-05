from statsmodels.iolib.smpickle import load_pickle
from sklearn.tree import DecisionTreeRegressor
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
    #with open('serialized_model.pkl', 'rb') as model_file:
    #    model = pickle.load(model_file)

    conn_string = f"host='{HOST}' port='{PORT}' dbname='{DB}' user='{USER}' password='{PASSWORD}'"
    conn = psycopg2.connect(conn_string)
    db_cursor = conn.cursor()

    #treino e predict da árvore
    db_cursor.execute("SELECT date_registered, price FROM dashboard_dolarprice ORDER BY date_registered DESC")
    train_data = db_cursor.fetchall()
    df_train = pd.DataFrame(train_data, columns=['date_registered', 'price'])
    df_temp= df_train[['price']].copy()
    p = 5
    for i in range(p):
        dftemp[f'price{i+1}'] = df_temp.price.shift(i+1)
    X = df_temp.drop('price', axis=1)
    y = df_temp.price
    model = DecisionTreeRegressor()
    model.fit(X, y)
    #fim dessa parte
    
    db_cursor.execute("SELECT date_registered, price FROM dashboard_dolarprice ORDER BY date_registered DESC LIMIT 60")
    data = db_cursor.fetchall()
    df_true = pd.DataFrame(data, columns=['date_registered', 'price'])
    
    forecast = model.predict(df_true.price)
    
    plt.plot(df_true)
    plt.plot(forecast)
    plot_image_path = "static/images/plot01.png"
    plt.savefig(plot_image_path)

    return forecast, plot_image_path
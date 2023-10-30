from django.shortcuts import render
from .fetch_data import fetch_data_from_api
from .models import DolarPrice
import pandas as pd

TABLE = 'dashboard_dolarprice'

# Create your views here.
def index(request):
    fetch_data_from_api(TABLE)
    dados = {"title": "Dolar Project"}

    dolar_prices = DolarPrice.objects.all()
    # Crie um dicionário para armazenar os valores de preço e data
    data = {
        "preco": [dolar.price for dolar in dolar_prices],
        "data": [dolar.date_registered for dolar in dolar_prices],
    }
    # Crie um DataFrame do Pandas com os dados
    dolar_all = pd.DataFrame(data)

    dolar_describe = dolar_all["preco"].describe()
    dolar_describe = dolar_describe.T.reset_index().values.tolist()
    statistics = ["count", "mean", "std", "min", "25%", "50%", "75%", "max"]
    num_statistics = [1, 2, 3, 4, 5, 6, 7, 8]
    dict = {}

    for i in range(len(dolar_describe)):
        dict[dolar_describe[i][0]] = round(dolar_describe[i][1], 3)

    dolar_primeiros = DolarPrice.objects.order_by("id").reverse()[:10]

    contexto = {
        "dados": dados,
        "dolar_primeiros": dolar_primeiros,
        "dolar_describe": dict,
        "statistics": statistics,
        "num_statistics": num_statistics,
        "dolar_all": dolar_all["preco"],
    }

    return render(request, "index.html", contexto)

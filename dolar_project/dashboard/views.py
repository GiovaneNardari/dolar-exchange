from django.shortcuts import render
from .fetch_data import fetch_data_from_api

TABLE = 'dashboard_dolarprice'

# Create your views here.
def index(request):
    fetch_data_from_api(TABLE)

    contexto = {
        "dados": {"title": "Dolar Project"}
    }

    return render(request, "index.html", contexto)

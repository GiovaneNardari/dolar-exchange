from django.shortcuts import render
from .fetch_data import fetch_data_from_api
from .model_prediction import predict_from_model

TABLE = 'dashboard_dolarprice'

# Create your views here.
def index(request):
    fetch_data_from_api(TABLE)

    contexto = {
        "dados": {"title": "Dolar Project"}
    }

    return render(request, "index.html", contexto)

def prediction_page(request):
    prediction, img_path = predict_from_model()

    contexto = {
        "dados": {"title": "Dolar Project", "prediction_result": prediction.values, "image_path": img_path}
    }

    return render(request, "prediction_page.html", contexto)
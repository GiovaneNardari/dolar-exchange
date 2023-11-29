from django.urls import path
from .views import index

urlpatterns = [
    path('', index),
    path('/predict', prediction_page)
]
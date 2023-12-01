from django.urls import path
from .views import index, prediction_page

urlpatterns = [
    path('', index),
    path('predict', prediction_page)
]
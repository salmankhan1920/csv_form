from django.urls import path
from . import views

urlpatterns = [
    path('order/', views.order_form, name='order_form'),
    path('display-csv/', views.display_csv, name='display_csv'),
    path('download-csv/', views.download_csv, name='download_csv'),
]




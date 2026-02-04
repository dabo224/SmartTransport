from django.urls import path
from . import views

urlpatterns = [
    path('traffic-dashboard/', views.predict_traffic, name='dashboard'),
]

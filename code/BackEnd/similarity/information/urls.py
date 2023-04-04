from django.urls import path, include
from . import views

urlpatterns = [
    path('getusername/',views.getusername),
    path('getallinfor/',views.getallinfor),
    path('changeinformation/', views.changeinformation),
    path('gethomeworkname/', views.gethomeworkname),
]
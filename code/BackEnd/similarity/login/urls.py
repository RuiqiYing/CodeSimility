from django.contrib import admin
from django.urls import path
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/',views.register),
    path('',views.login),
    path('pwd_update/',views.pwd_update)
]
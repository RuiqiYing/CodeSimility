from django.contrib import admin
from django.urls import path
from django.urls import path, include
from . import views

urlpatterns = [
    path('creat/',views.creat),
    path('list/',views.list),
    path('delete/',views.delete),

]
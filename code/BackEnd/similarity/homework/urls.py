
from django.urls import path, include
from . import views

urlpatterns = [
    path('creat/',views.creat),
    path('list/',views.list),
    path('delete/',views.delete),
    path('gethomework/', views.gethomework),
    path('submit/',views.submit),
    path('submitcode/',views.submitcode),
]
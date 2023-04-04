from django.urls import path, include
from . import views

urlpatterns = [
    path('join/',views.joinCourse),
    path('viewStuCourse/',views.viewStuCourse),
    path('getquestionlist/',views.getquestionlist),
]
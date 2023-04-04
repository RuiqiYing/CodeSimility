
from django.urls import path, include
from . import views

urlpatterns = [
    path('gethomework/',views.gethomework),
    path('getsum/',views.getsum),
    path('compare/',views.compare),
    path('getsimdetail/', views.getsimdetail),
    path('getstuhomeworksim/', views.getstuhomeworksim),
]
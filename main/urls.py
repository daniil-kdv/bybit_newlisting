# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new-listing/', views.new_listing, name='new_listing'),
]


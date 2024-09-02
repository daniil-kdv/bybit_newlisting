from django.contrib import admin
from django.urls import path, include  
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('new-listing/', views.new_listing, name='new_listing'),
    path('rsi-heatmap/', views.rsi_heatmap, name='rsi_heatmap'),
    path('notice/', views.notice, name='notice'),
    path('news_feed/', views.news_feed, name='news_feed'),
]


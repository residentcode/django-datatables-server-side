from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_view, name='home'),
    path('file/', views.data_tables_json_file, name='file'),
]
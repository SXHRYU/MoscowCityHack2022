from django.urls import path
from .views import index_view

urlpatterns = [
    path('index/', index_view, name='index_view'),
    path('', index_view, name='index_view'),
]

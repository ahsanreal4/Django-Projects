from django.urls import path
from .views import index, about, menu


urlpatterns = [
    path('', index),
    path('about', about),
    path('menu', menu),

]

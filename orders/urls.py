from django.urls import path
from . import views


urlpatterns = [
    path('place-orders/', views.place_order, name='place-order'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create-shoe/', views.createShoe, name="create-shoe"),
    path('delete-shoe/<str:pk>/', views.deleteShoe, name="delete-shoe"),
    path('update-shoe/<str:pk>/', views.updateShoe, name="update-shoe"),
    path('checkout/<str:pk>/', views.checkout, name="checkout"),
]
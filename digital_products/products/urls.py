from django.contrib import admin
from django.urls import path

from .views import ProductListView, ProductDetailsView
urlpatterns = [
    path('products/', ProductListView.as_view()),
    path('products/<int:id>/', ProductDetailsView.as_view()),
]
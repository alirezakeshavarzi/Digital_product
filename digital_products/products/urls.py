from django.contrib import admin
from django.urls import path

from .views import ProductListView
urlpatterns = [
    path('products/', ProductListView.as_view()),
    #path('categores/', CategoryListView.as_view()),
]
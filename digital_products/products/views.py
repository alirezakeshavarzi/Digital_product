from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Product, File, Category

from .serializers import ProductSerializer

class ProductListView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

'''class CategoryListView(APIView):

    def get(self, request):
        categorys = Category.objects.all()
        serializer = Serializer(categorys,many=True)
        return Response(serializer.data)
'''



# Create your views here.

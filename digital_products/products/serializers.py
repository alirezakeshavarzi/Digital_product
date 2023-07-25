from rest_framework import serializers

from .models import Product, Category, File

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','title', 'description', 'avatar', 'file')

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ('id','title', 'file')

class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ('id','title', 'description', 'avatar', 'categories')

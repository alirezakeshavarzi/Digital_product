from django.contrib import admin

from .models import Category, File, Product

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(File)

# Register your models here.

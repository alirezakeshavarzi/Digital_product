from django.contrib import admin

from .models import Category, File, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_enable', 'create_time']
    list_filter = ['is_enable']
    search_fields = ['title'] # search in titles(in database)

#@admin.register(File)
class FileInlineAdmin(admin.StackedInline):
    model = File
    fields = ['title', 'file', 'is_enable']
    extra = 0



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_enable', 'create_time']
    list_filter = ['is_enable']
    search_fields = ['title']
    #filter_horizontal = ['categories'] # show filter horizontal categories
    #inlines = FileInlineAdmin


# Register your models here.

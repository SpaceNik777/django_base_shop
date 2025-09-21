from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий
    list_display - поля для отображения (['name', 'slug'])
    prepopulated_fields - поля для автоматического заполнения (slug: ('name',))
    """
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Админка для товаров
    list_display - поля для отображения (['name', 'category', 'price', 'available', 'created', 'updated'])
    list_filter - поля для фильтрации (['available', 'created', 'updated', 'category'])
    list_editable - поля для редактирования (['price', 'available'])
    prepopulated_fields - поля для автоматического заполнения (slug: ('name',))
    """
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

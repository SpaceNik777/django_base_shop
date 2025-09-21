from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    """Категории товаров
    slug - уникальный идентификатор категории (unique=True - для уникальности)
    name - название категории (db_index=True - для ускорения поиска)
    """
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        """Метаданные категории
        ordering - сортировка категорий по названию
        verbose_name - название категории в единственном числе
        verbose_name_plural - название категории во множественном числе
        """
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    
    def __str__(self):
        """Строковое представление категории (возвращает название категории в виде строки)
        """
        return self.name
    
    def get_absolute_url(self):
        """Получить абсолютный URL для категории (возвращает URL категории в виде строки)
        """
        return reverse('main:product_list_by_category', args=[self.slug])

class Product(models.Model):
    """Товары
    category - категория товара (ForeignKey - связь с моделью Category) 
    (related_name='products' - имя обратной связи) 
    (on_delete=models.CASCADE - при удалении категории, удаляются все товары, есть еще SET_NULL, PROTECT, RESTRICT)
    name - название товара (max_length=100 - максимальная длина названия) (db_index=True - для ускорения поиска)
    slug - уникальный идентификатор товара (max_length=100 - максимальная длина идентификатора) (unique=True - для уникальности)
    image - изображение товара (upload_to='products/%Y/%m/%d' - путь к изображению) (blank=True - для возможности не загружать изображение)
    description - описание товара (blank=True - для возможности не загружать описание)
    price - цена товара (max_digits=10 - максимальное количество цифр) (decimal_places=2 - количество цифр после запятой)
    available - доступность товара (default=True - для возможности не загружать доступность)
    created - дата создания товара (auto_now_add=True - для автоматического добавления даты создания)
    updated - дата обновления товара (auto_now=True - для автоматического добавления даты обновления)
    """
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=100, unique=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        """Метаданные товара
        ordering - сортировка товаров по названию
        """
        ordering = ('name',)

    def __str__(self):
        """Строковое представление товара (возвращает название товара в виде строки)
        """
        return self.name

    def get_absolute_url(self):
        """Получить абсолютный URL для товара (возвращает URL товара в виде строки)
        """
        return reverse('main:product_detail', args=[self.id, self.slug])
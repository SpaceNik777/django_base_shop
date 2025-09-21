from django.shortcuts import render, get_object_or_404
from .models import Category, Product


# Create your views here.
def product_list(request, category_slug=None):
    """Список товаров
    categories - все категории (Category.objects.all())
    products - все товары (Product.objects.filter(available=True))
    category - текущая категория (get_object_or_404(Category, slug=category_slug))
    """
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'main/product/list.html', 
                    {'categories': categories, 
                    'products': products, 
                    'category': category})

def product_detail(request, id, slug):
    """Детальная страница товара
    product - товар (get_object_or_404(Product, id=id, slug=slug))
    related_products - связанные товары (Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4])
    """
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    return render(request, 'main/product/detail.html', {'product': product, 'related_products': related_products})
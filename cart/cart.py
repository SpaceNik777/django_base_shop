from django.conf import settings
from main.models import Product
from decimal import Decimal

class Cart:
    def __init__(self, request):
        """Инициализация корзины
        request.session - сессия пользователя
        cart - корзина пользователя
        if not cart: - если корзина не существует, то создаем ее
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """Добавление товара в корзину
        product - товар
        quantity - количество товара
        override_quantity - перезаписать количество товара
        product_id - id товара
        if product_id not in self.cart: - если товар не существует в корзине, то создаем его
        self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity: - если перезаписать количество товара, то записываем его
            self.cart[product_id]['quantity'] = quantity
        else: - если не перезаписать количество товара, то добавляем его
            self.cart[product_id]['quantity'] += quantity
        self.save()
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Сохранение корзины
        self.session.modified = True - устанавливаем флаг, что сессия изменена
        """
        self.session.modified = True

    def remove(self, product):
        """Удаление товара из корзины
        product - товар
        product_id - id товара
        if product_id in self.cart: - если товар существует в корзине, то удаляем его
            del self.cart[product_id]
        self.save()
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Итерация по корзине
        product_ids - список id товаров
        products - список товаров
        cart - корзина
        for product in products: - для каждого товара в списке
            cart[str(product.id)]['product'] = product - добавляем товар в корзину
        for item in cart.values(): - для каждого элемента в корзине
            item['price'] = Decimal(item['price']) - преобразуем цену в Decimal
            item['total_price'] = item['price'] * item['quantity'] - вычисляем общую цену
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Количество товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Общая цена товаров в корзине"""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Очистка корзины
        del self.session[settings.CART_SESSION_ID] - удаляем корзину из сессии
        self.save() - сохраняем корзину
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
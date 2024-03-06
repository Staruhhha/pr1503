from django.db import models
from django.urls import reverse_lazy
MAX_LENGTH_CHAR = 255

class Supplier(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название')
    representor_surname = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Фамилия представителя')
    representor_name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Имя представителя')
    representor_patronymic = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Отчество представителя')
    representor_phone_number = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Телефон представителя')
    address = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Адрес')
    isActive = models.BooleanField(default=True, verbose_name='Существует ли?')

    def __str__(self):
        return (f"{self.name}, представитель: {self.representor_surname} {self.representor_name}"
                f" {self.representor_patronymic}, телефон: {self.representor_phone_number}")

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'

class Supply(models.Model):
    date = models.DateTimeField(verbose_name='Дата поставки')

    supplier = models.ForeignKey(Supplier, on_delete=models.PROTECT, verbose_name='Поставщик')
    product = models.ManyToManyField('Product', through='Pos_supply', verbose_name='Товар')

    def __str__(self):
        return f"{self.pk} - {self.date}, название компании-поставщика: {self.supplier.name}"

    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'

class Pos_supply(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Товар')
    supply = models.ForeignKey(Supply, on_delete=models.PROTECT, verbose_name='Поставка')

    quantity = models.PositiveIntegerField(verbose_name='Количество товара')

    def __str__(self):
        return f"{self.product.name} - {self.supply.pk}"

    class Meta:
        verbose_name = 'Позиция поставки'
        verbose_name_plural = 'Позиции поставок'


class Tag(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Category(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def get_absolute_url(self):
        return reverse_lazy('category_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Order(models.Model):
    SHOP = "SH"
    COURIER = "CR"
    PICKUPPOINT = "PP"

    TYPE_OF_DELIVERY = [
        (SHOP, "Магазин"),
        (COURIER, "Курьер"),
        (PICKUPPOINT, "Пункт выдачи")
    ]

    customer_surname = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Фамилия покупателя')
    customer_name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Имя покупателя')
    customer_patronymic = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Отчество покупателя')
    delivery_address = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Адрес доставки')
    delivery_type = models.CharField(max_length=2, choices=TYPE_OF_DELIVERY, default=SHOP, verbose_name='Способ доставки')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    finish_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата создания')

    product = models.ManyToManyField('Product', through='Pos_order', verbose_name='Товар')

    def __str__(self):
        return f"{self.pk}: {self.customer_surname} {self.customer_name} {self.customer_patronymic}, {self.creation_date}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        permissions = [
            ('change_delivery_type', 'Возможность изменить тип доставки'),
        ]

from shop.utils import sum_price_count
class Pos_order(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Товар')
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ')
    quantity = models.PositiveIntegerField(default=1,verbose_name='Количество товара')
    discount = models.PositiveIntegerField(default=0, verbose_name='Скидка')

    def __str__(self):
        return f"{self.pk} - {self.product.name}, {self.order.customer_surname} {self.order.customer_name} {self.order.customer_patronymic}"

    def sum_pos_order(self):
        return sum_price_count(self.product.price, self.quantity, self.discount)

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'

class Parameter(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'

class Pos_parameter(models.Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT, verbose_name='Товар')
    parameter = models.ForeignKey(Parameter, on_delete=models.PROTECT, verbose_name='Характеристика')
    value = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Значение характеристики')


    def __str__(self):
        return f"{self.product.name} - {self.value}"

    class Meta:
        verbose_name = 'Позиция характеристики'
        verbose_name_plural = 'Позиции характеристик'

class Product(models.Model):
    name = models.CharField(max_length=MAX_LENGTH_CHAR, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    image = models.ImageField(upload_to='image/%Y/%m/%d', null=True, blank=True, verbose_name='Картинка')
    isActive = models.BooleanField(default=True, verbose_name='Существует ли?')

    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    tag = models.ManyToManyField(Tag, blank=True, null=True)
    parameter = models.ManyToManyField(Parameter, through=Pos_parameter)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
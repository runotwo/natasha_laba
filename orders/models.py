from django.contrib.auth.models import User
from django.db import models

from goods.models import Good


class Address(models.Model):
    city = models.CharField(verbose_name='Город', max_length=255)
    street = models.CharField(verbose_name='Улица', max_length=255)
    house_number = models.PositiveIntegerField(verbose_name='Номер дома')
    apartment_number = models.PositiveIntegerField(verbose_name='Номер квартиры')

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f'{self.city}, ул. {self.street}, д.{self.house_number}/{self.apartment_number}'


class Order(models.Model):
    STATUS_CHOICES = (
        ('created', 'Создан'),
        ('payed', 'Оплачен'),
        ('canceled', 'Отменен'),
        ('delivering', 'Доставляется'),
        ('delivered', 'Доставлен')
    )
    client = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    status = models.CharField(verbose_name='Статус', max_length=30,
                              blank=False, choices=STATUS_CHOICES,
                              null=False, default='created')
    address = models.ForeignKey(Address, verbose_name='Адрес', on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('created_at',)

    def get_total_price(self):
        return self.orderitem_set.all().aggregate(price=models.Sum(models.F('good__price') * models.F('count'),
                                                                   output_field=models.FloatField()))['price']

    def __str__(self):
        return f'{self.client}({self.id})'


class OrderItem(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.count > 0:
            super(OrderItem, self).save(*args, **kwargs)
        else:
            super(OrderItem, self).save(*args, **kwargs)
            self.delete()

    def __str__(self):
        return self.good.name

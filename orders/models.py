from django.contrib.auth.models import User
from django.db import models

from goods.models import Good


class Order(models.Model):
    client = models.ForeignKey(User, verbose_name='Покупатель', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(verbose_name='Время создания', auto_now_add=True)
    canceled = models.BooleanField(verbose_name='Отменен', default=False)
    confirmed = models.BooleanField(verbose_name='Подтвержден', default=False)
    confirmed_at = models.DateTimeField(verbose_name='Время оплаты', auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ('-created_at', )

    def get_total_price(self):
        return self.orderitem_set.all().aggregate(price=models.Sum(models.F('price')*models.F('count'),
                                                                   output_field=models.FloatField()))['price']


class OrderItem(models.Model):
    good = models.ForeignKey(Good, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
from django.contrib.auth.models import User
from django.db import models

from orders.models import Address


class Config(models.Model):
    SEX = [('m', 'M'), ('f', 'Ж')]
    address = models.ForeignKey(Address, verbose_name='Адрес', on_delete=models.SET_NULL, null=True, default=None)
    number = models.CharField(verbose_name='Номар телефона', max_length=255, null=True, default='')
    user = models.OneToOneField(User, models.CASCADE, null=True)
    sex = models.CharField(verbose_name='Пол', max_length=30,
                           blank=False, choices=SEX,
                           null=False, default='f')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

import uuid

from django.db import models


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    return "%s.%s" % (uuid.uuid4(), ext)


class Category(models.Model):
    name = models.CharField(max_length=63, verbose_name='Наименование', unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Good(models.Model):
    name = models.CharField(max_length=63, verbose_name='Наименование')
    category = models.ForeignKey(Category, verbose_name='Категория', related_name='goods', null=True, blank=False,
                                 on_delete=models.SET_NULL)
    count = models.PositiveIntegerField(default=0, verbose_name='Количество')
    image = models.ImageField(blank=False, null=True, upload_to=get_file_path, verbose_name='Изображение')
    price = models.PositiveIntegerField(default=10, verbose_name='Стоимость')
    description = models.CharField(max_length=500, verbose_name='Описание', default='')
    cost_price = models.PositiveIntegerField(default=8, verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

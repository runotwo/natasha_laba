# Generated by Django 2.0.5 on 2018-10-31 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20181018_0729'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='index',
            field=models.PositiveIntegerField(null=True, verbose_name='Индекс'),
        ),
    ]
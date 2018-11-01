# Generated by Django 2.0.5 on 2018-10-31 22:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_address_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Создан'), ('await', 'Ожидается оплата'), ('payed', 'Оплачен'), ('canceled', 'Отменен'), ('delivering', 'Доставляется'), ('delivered', 'Доставлен')], default='created', max_length=30, verbose_name='Статус'),
        ),
    ]

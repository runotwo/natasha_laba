# Generated by Django 2.0.5 on 2018-10-18 01:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=255, verbose_name='Город')),
                ('street', models.CharField(max_length=255, verbose_name='Улица')),
                ('house_number', models.PositiveIntegerField(verbose_name='Номер дома')),
                ('apartment_number', models.PositiveIntegerField(verbose_name='Номер квартиры')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=63, verbose_name='Статус')),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='canceled',
        ),
        migrations.RemoveField(
            model_name='order',
            name='confirmed',
        ),
        migrations.RemoveField(
            model_name='order',
            name='confirmed_at',
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('created', 'Создан'), ('payed', 'Оплачен'), ('canceled', 'Отменен'), ('delivering', 'Доставляется'), ('delivered', 'Доставлен')], default='created', max_length=30, verbose_name='Статус'),
        ),
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.Address', verbose_name='Адрес'),
        ),
    ]

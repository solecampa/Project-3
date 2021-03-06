# Generated by Django 3.0.7 on 2020-06-04 03:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_delete_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='initiated', max_length=64)),
                ('pedidos', models.ManyToManyField(blank=True, related_name='orden', to='orders.Pedido')),
            ],
        ),
    ]

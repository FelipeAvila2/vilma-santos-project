# Generated by Django 5.0.1 on 2024-02-22 13:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0005_venda_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='vendas.cliente'),
        ),
    ]

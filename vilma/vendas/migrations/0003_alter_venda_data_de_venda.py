# Generated by Django 5.0.1 on 2024-02-22 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0002_venda_data_de_venda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='data_de_venda',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]

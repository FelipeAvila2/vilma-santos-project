# Generated by Django 5.0.1 on 2024-02-22 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendas', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='data_de_venda',
            field=models.DateField(null=True),
        ),
    ]

# Generated by Django 5.0.1 on 2024-02-24 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventorio', '0003_remove_ingrediente_produtos_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingrediente',
            name='quantidade',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
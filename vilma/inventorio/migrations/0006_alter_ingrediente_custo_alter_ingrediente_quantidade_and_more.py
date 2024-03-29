# Generated by Django 5.0.1 on 2024-02-24 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventorio', '0005_alter_ingredienteordemdecompra_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingrediente',
            name='custo',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ingrediente',
            name='quantidade',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ingredienteordemdecompra',
            name='quantity',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='ingredienttransaction',
            name='quantity',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='inventorytransaction',
            name='quantity',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='produto',
            name='preco',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
        migrations.AlterField(
            model_name='produtoingrediente',
            name='quantidade',
            field=models.DecimalField(decimal_places=4, max_digits=10),
        ),
    ]

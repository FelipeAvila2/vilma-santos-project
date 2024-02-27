# Generated by Django 5.0.1 on 2024-02-07 17:41

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Fornecedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=20)),
                ('endereco', models.CharField(max_length=100)),
                ('contato', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Ingrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=40)),
                ('unidade_de_medida', models.CharField(choices=[('L', 'Litros'), ('Kg', 'Quilos'), ('Un', 'Unidades')], max_length=2)),
                ('quantidade', models.IntegerField()),
                ('custo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ordem_de_compra', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='IngredienteOrdemDeCompra',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorio.ingrediente')),
            ],
        ),
        migrations.CreateModel(
            name='IngredientTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_number', models.CharField(max_length=20, unique=True)),
                ('transaction_type', models.CharField(choices=[('T', 'Transferencia'), ('Rc', 'Recebido'), ('A', 'Ajuste'), ('Rt', 'Retorno'), ('D', 'Descartado'), ('U', 'Usado')], max_length=20)),
                ('transaction_date', models.DateField(default=django.utils.timezone.now)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorio.ingrediente')),
            ],
        ),
        migrations.CreateModel(
            name='InventoryTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_number', models.CharField(max_length=20, unique=True)),
                ('transaction_type', models.CharField(choices=[('T', 'Transferencia'), ('Rc', 'Recebido'), ('A', 'Ajuste'), ('Rt', 'Retorno'), ('D', 'Descartado'), ('V', 'Venda')], max_length=20)),
                ('transaction_date', models.DateField(default=django.utils.timezone.now)),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorio.produto')),
            ],
        ),
        migrations.CreateModel(
            name='ProdutoIngrediente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.IntegerField()),
                ('ingrediente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorio.ingrediente')),
                ('produto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventorio.produto')),
            ],
        ),
        migrations.AddField(
            model_name='produto',
            name='ingredientes',
            field=models.ManyToManyField(through='inventorio.ProdutoIngrediente', to='inventorio.ingrediente'),
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='produtos',
            field=models.ManyToManyField(through='inventorio.ProdutoIngrediente', to='inventorio.produto'),
        ),
        migrations.CreateModel(
            name='PurchaseOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20, unique=True)),
                ('order_date', models.DateField(default=django.utils.timezone.now)),
                ('delivery_date', models.DateField()),
                ('status', models.CharField(choices=[('P', 'Pendente'), ('R', 'Recebido'), ('PG', 'Pago')], default='pendente', max_length=20)),
                ('ingredients', models.ManyToManyField(related_name='purchase_orders', through='inventorio.IngredienteOrdemDeCompra', to='inventorio.ingrediente')),
                ('supplier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorio.fornecedor')),
            ],
        ),
        migrations.AddField(
            model_name='ingredienteordemdecompra',
            name='ordem_de_compra',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorio.purchaseorder'),
        ),
        migrations.AddField(
            model_name='ingrediente',
            name='ordens_de_compra',
            field=models.ManyToManyField(through='inventorio.IngredienteOrdemDeCompra', to='inventorio.purchaseorder'),
        ),
    ]
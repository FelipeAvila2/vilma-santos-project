# Generated by Django 5.0.1 on 2024-02-26 17:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventorio', '0006_alter_ingrediente_custo_alter_ingrediente_quantidade_and_more'),
        ('vendas', '0006_alter_venda_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='venda',
            name='desconto',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.CreateModel(
            name='Orcamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('desconto', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('produtos', models.ManyToManyField(related_name='budget_proposals', to='inventorio.produto')),
            ],
        ),
        migrations.CreateModel(
            name='BudgetProposalItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField()),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventorio.produto')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendas.orcamento')),
            ],
        ),
    ]

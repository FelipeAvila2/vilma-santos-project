from django.urls import path, include
from .views import (lista_de_clientes, novo_cliente, lista_de_vendas, nova_venda, delete_venda, download_csv_report,
                    edit_cliente, delete_cliente, create_budget_proposal, lista_orcamentos, generate_pdf, edit_orcamento,
                    delete_orcamento)

urlpatterns = [
    path('lista_de_clientes/', lista_de_clientes, name='lista_de_clientes'),
    path('novo_cliente/', novo_cliente, name='novo_cliente'),
    path('lista_de_vendas/', lista_de_vendas, name='lista_de_vendas'),
    path('nova_venda/', nova_venda, name='nova_venda'),
    path('delete_venda/<int:venda_id>/', delete_venda, name='delete_venda'),
    path('delete_cliente/<int:cliente_id>/', delete_cliente, name='delete_cliente'),
    path('edit_cliente/<int:cliente_id>/', edit_cliente, name='edit_cliente'),
    path('download-csv/', download_csv_report, name='download_csv_report'),
    path('orcamento/', create_budget_proposal, name='orcamento'),
    path('edit_orcamento/<int:orcamento_id>/', edit_orcamento, name='edit_orcamento'),
    path('delete_orcamento/<int:orcamento_id>/', delete_orcamento, name='delete_orcamento'),
    path('lista_de_orcamentos/', lista_orcamentos, name='lista_de_orcamentos'),
    path('generate_pdf/<int:orcamento_id>/', generate_pdf, name='generate_pdf'),
]


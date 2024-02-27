from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (inventory_transaction_list, create_inventory_transaction,
                    supplier_list, product_list, ingredient_list, purchase_order_list,
                    create_supplier, create_product, create_purchase_order, create_ingredient, OrderIngredientsAPIView,
                    edit_product, delete_product, edit_supplier, delete_supplier, get_product_price)

router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('transacoes/', inventory_transaction_list, name='transaction_list'),
    path('transacoes/nova/', create_inventory_transaction, name='create_transaction'),
    path('fornecedores/', supplier_list, name='supplier_list'),
    path('produtos/', product_list, name='product_list'),
    path('ingredientes/', ingredient_list, name='ingredient_list'),
    path('purchase_orders/', purchase_order_list, name='purchaseorder_list'),
    path('create_supplier/', create_supplier, name='create_supplier'),
    path('create_product/', create_product, name='create_product'),
    path('create_purchase_order/', create_purchase_order, name='create_purchase_order'),
    path('create_ingredient/', create_ingredient, name='create_ingredient'),
    path('api/orders/<int:order_id>/ingredients/', OrderIngredientsAPIView.as_view(), name='order_ingredients_api'),
    path('edit/<int:product_id>/', edit_product, name='edit_product'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path('edit_supplier/<int:supplier_id>/', edit_supplier, name='edit_supplier'),
    path('delete_supplier/<int:supplier_id>/', delete_supplier, name='delete_supplier'),
    path('get_product_price/<int:product_id>/', get_product_price, name='get_product_price'),
]
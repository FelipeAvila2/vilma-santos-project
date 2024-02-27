
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory, inlineformset_factory
from django.db.models import Sum, Avg, Value, DecimalField
from django.db.models.functions import Coalesce
from .models import (InventoryTransaction, Fornecedor, Produto, Ingrediente, PurchaseOrder,
                     ProdutoIngrediente, IngredienteOrdemDeCompra)
from .forms import (InventoryTransactionForm, FornecedorForm, ProdutoForm, PurchaseOrderForm,
                    IngredienteForm, IngredienteFormSet)

from rest_framework.views import APIView
from rest_framework.response import Response
from .models import IngredienteOrdemDeCompraSerializer
from django.http import HttpResponseBadRequest
from django.db.models import Sum
from django.db.models import F, ExpressionWrapper, DecimalField
from django.db.models.functions import TruncMonth  # Import TruncMonth

def inventory_transaction_list(request):
    transactions = InventoryTransaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})


def create_inventory_transaction(request):
    if request.method == 'POST':
        form = InventoryTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = InventoryTransactionForm()
    return render(request, 'create_transaction.html', {'form': form})


def supplier_list(request):
    suppliers = Fornecedor.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})


def product_list(request):
    products = Produto.objects.prefetch_related('produtoingrediente_set__ingrediente').all()
    return render(request, 'product_list.html', {'products': products})


def edit_product(request, product_id):
    product = get_object_or_404(Produto, pk=product_id)

    # Get queryset of existing ProdutoIngrediente instances related to the Produto
    queryset = ProdutoIngrediente.objects.filter(produto=product)

    ingrediente_formset = inlineformset_factory(Produto, ProdutoIngrediente, formset=IngredienteFormSet,
                                               fields=('ingrediente', 'quantidade'), extra=1)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=product)
        formset = ingrediente_formset(request.POST, queryset=queryset)

        if form.is_valid() and formset.is_valid():
            form.save()

            for ingrediente_form in formset:
                if ingrediente_form.cleaned_data:
                    ingrediente_data = ingrediente_form.cleaned_data
                    ingrediente_id = ingrediente_data['ingrediente'].id
                    ingrediente_instance = queryset.filter(ingrediente=ingrediente_id).first()

                    if ingrediente_instance:
                        # Update existing instance
                        ingrediente_instance.quantidade = ingrediente_data['quantidade']
                        ingrediente_instance.save()
                    else:
                        # Create new instance and associate with the product
                        ingrediente_instance = ingrediente_form.save(commit=False)
                        ingrediente_instance.produto = product
                        ingrediente_instance.save()
            return redirect('product_list')
    else:
        form = ProdutoForm(instance=product)
        formset = ingrediente_formset(queryset=queryset)

    return render(request, 'edit_product.html', {'form': form, 'ingrediente_formset': formset})



def delete_product(request, product_id):
    product = get_object_or_404(Produto, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'delete_product.html', {'product': product})


def ingredient_list(request):
    ingredients = Ingrediente.objects.values('nome').annotate(
        total_quantity=Sum('quantidade'),
        avg_cost=Avg(Coalesce('custo', 0), output_field=DecimalField()),
    )

    for ingredient in ingredients:
        ingredient['avg_cost'] = round(ingredient['avg_cost'], 2)

    print(ingredients)  # Print queryset for debugging

    return render(request, 'ingredient_list.html', {'ingredients': ingredients})


def purchase_order_list(request):
    purchase_orders = PurchaseOrder.objects.all()

    # Calculate total cost for each purchase order
    for order in purchase_orders:
        total_cost_expression = ExpressionWrapper(F('ingrediente__custo') * F('ingrediente__quantidade'), output_field=DecimalField())
        total_cost = order.ingredienteordemdecompra_set.annotate(total_cost=total_cost_expression).aggregate(
            total=Sum('total_cost'))['total'] or 0
        order.total_cost = total_cost

    # Calculate total expenses aggregated by month
    total_expense_by_month = PurchaseOrder.objects.annotate(month=TruncMonth('order_date')).values('month').annotate(total_expense=Sum(F('ingrediente__custo') * F('ingrediente__quantidade')))

    # Convert the queryset into a dictionary where keys are month names and values are total expenses
    total_expense_by_month_dict = {expense['month'].strftime('%B'): expense['total_expense'] for expense in total_expense_by_month}

    return render(request, 'purchaseorder_list.html', {'purchase_orders': purchase_orders, 'total_expense_by_month': total_expense_by_month_dict})


def create_supplier(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = FornecedorForm()
    return render(request, 'create_supplier.html', {'form': form})


def edit_supplier(request, supplier_id):
    supplier = get_object_or_404(Fornecedor, pk=supplier_id)
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = FornecedorForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form})


def delete_supplier(request, supplier_id):
    supplier = get_object_or_404(Fornecedor, pk=supplier_id)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'confirm_supplier_delete.html', {'supplier': supplier})

def create_product(request):
    if request.method == 'POST':
        produto_form = ProdutoForm(request.POST)
        ingrediente_formset = IngredienteFormSet(request.POST)

        if produto_form.is_valid() and ingrediente_formset.is_valid():
            produto = produto_form.save()
            for form in ingrediente_formset:
                ingrediente = form.save(commit=False)
                ingrediente.produto = produto
                ingrediente.save()

            return redirect('product_list')
    else:
        produto_form = ProdutoForm()
        unique_ingredientes = ProdutoIngrediente.objects.order_by('ingrediente').distinct('ingrediente')
        ingrediente_formset = IngredienteFormSet(queryset=unique_ingredientes)

    return render(request, 'create_product.html', {'produto_form': produto_form,
                                                   'ingrediente_formset': ingrediente_formset})


class OrderIngredientsAPIView(APIView):
    def get(self, request, order_id):
        ingredients = IngredienteOrdemDeCompra.objects.filter(ordem_de_compra_id=order_id)
        serializer = IngredienteOrdemDeCompraSerializer(ingredients, many=True)
        return Response(serializer.data)


def create_purchase_order(request):
    IngredienteFormSet = formset_factory(IngredienteForm, extra=1)
    all_fornecedores = Fornecedor.objects.all()
    ingredient_choices = Ingrediente.TIPOS_DE_UNIDADE.items()  # Choices for unit of measure field

    if request.method == 'POST':
        purchase_order_form = PurchaseOrderForm(request.POST)
        ingredient_formset = IngredienteFormSet(request.POST)

        if purchase_order_form.is_valid() and ingredient_formset.is_valid():
            purchase_order = purchase_order_form.save(commit=False)  # Don't save to database yet
            fornecedor_instance = purchase_order_form.cleaned_data.get('supplier')
            purchase_order.save()  # Now save to database

            # Save ingredient formset
            for form in ingredient_formset:
                if form.is_valid():
                    ingredient = form.save(commit=False)
                    ingredient.save()  # Save the ingredient first
                    ingredient_ordem = IngredienteOrdemDeCompra.objects.create(
                        ingrediente=ingredient,
                        ordem_de_compra=purchase_order,
                        quantity=ingredient.quantidade
                    )

            return redirect('purchaseorder_list')
        else:
            # Handle form validation errors
            print("Form validation errors:", purchase_order_form.errors)
            print("Ingredient formset errors:", ingredient_formset.errors)
    else:
        purchase_order_form = PurchaseOrderForm()
        ingredient_formset = IngredienteFormSet()

    return render(request, 'create_purchase_order.html', {
        'purchase_order_form': purchase_order_form,
        'ingredient_formset': ingredient_formset,
        'all_fornecedores': all_fornecedores,
        'ingredient_choices': ingredient_choices,
    })



def create_ingredient(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ingredient_list')
    else:
        form = IngredienteForm()
    return render(request, 'create_ingredient.html', {'form': form})


def get_product_price(request, product_id):
    try:
        produto = Produto.objects.get(pk=product_id)
        price = produto.preco
        return JsonResponse({'price': price})
    except Produto.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
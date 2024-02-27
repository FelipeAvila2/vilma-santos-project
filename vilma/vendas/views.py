from django.shortcuts import redirect
from django.db.models import Sum
from .models import Cliente, Venda
from .forms import ClienteForm, VendaForm, OrcamentoForm
from producao.models import Estoque
import datetime
from calendar import month_name
import csv
from django.http import HttpResponse
from .forms import BudgetProposalItemForm, BudgetProposalItemFormSet
from .models import Orcamento, BudgetProposalItem
from django.shortcuts import get_object_or_404, render
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from django.forms import inlineformset_factory


def edit_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes')  # Redirect to the clients list view
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'edit_cliente.html', {'form': form, 'cliente': cliente})

def delete_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        cliente.delete()
    return redirect('clientes')  # Redirect to the clients list view


def download_csv_report(request):
    vendas = Venda.objects.all()  # Adjust if needed
    return generate_csv_report(vendas)

def generate_csv_report(vendas):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Data de Venda', 'Cliente', 'Quantidade', 'Custo', 'Preço', 'Lucro Operacional'])  # Write header row

    for venda in vendas:
        custo = venda.estoque.produto.calcular_custo() if venda.estoque.produto else 0
        lucro_operacional = venda.preco - custo
        writer.writerow([venda.id, venda.data_de_venda, venda.cliente, venda.quantidade, custo, venda.preco, lucro_operacional])

    return response

def delete_venda(request, venda_id):
    venda = get_object_or_404(Venda, pk=venda_id)
    if request.method == 'POST':
        venda.delete()
        return redirect('lista_de_vendas')  # Redirect to the list of sales after deletion
    return render(request, 'delete_venda.html', {'venda': venda})

def lista_de_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

def novo_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_de_clientes')
    else:
        form = ClienteForm()
    return render(request, 'novo_cliente.html', {'form': form})

def lista_de_vendas(request):
    sort_by = request.GET.get('sort')

    if sort_by == 'date':
        vendas = Venda.objects.order_by('data_de_venda')
    else:
        vendas = Venda.objects.all()

    # Calculate total profit aggregated by month for current and past months
    now = datetime.datetime.now()
    current_month = now.month

    total_profit_by_month = {}
    for month in range(1, current_month + 1):
        month_name_str = month_name[month]
        total_profit = Venda.objects.filter(data_de_venda__month=month).aggregate(total_profit=Sum('preco'))['total_profit'] or 0
        total_profit_by_month[month_name_str] = total_profit

    return render(request, 'vendas.html', {'vendas': vendas, 'total_profit_by_month': total_profit_by_month})

def nova_venda(request):
    if request.method == 'POST':
        form = VendaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_de_vendas')
    else:
        form = VendaForm()

        # Calculate initial price based on the selected product and quantity
        produto_id = request.GET.get('produto_id')
        quantidade = request.GET.get('quantidade')
        if produto_id and quantidade:
            # Assuming you have models and relationships properly set up
            # Adjust this part based on your actual model structure
            estoque = get_object_or_404(Estoque, pk=produto_id)
            preco = estoque.produto.preco * int(quantidade)
            form.fields['preco'].initial = preco

    return render(request, 'nova_venda.html', {'form': form})


def create_budget_proposal(request):
    if request.method == 'POST':
        item_formset = BudgetProposalItemFormSet(request.POST)

        print("POST data:", request.POST)
        print("Formset errors:", item_formset.errors)
        print("Formset is valid:", item_formset.is_valid())

        if item_formset.is_valid():
            proposal = Orcamento.objects.create()  # Create an empty proposal
            total_cost = 0

            for form in item_formset:
                item = form.save(commit=False)
                item.proposal = proposal
                item.save()
                total_cost += item.cost()

            proposal.total_cost = total_cost
            proposal.save()

            return redirect('lista_de_orcamentos')  # Redirect to success page or any other desired action
    else:
        item_formset = BudgetProposalItemFormSet()

    return render(request, 'orcamento.html', {'item_formset': item_formset})


def lista_orcamentos(request):
    orcamentos = Orcamento.objects.all()
    for orcamento in orcamentos:
        orcamento.total_cost = sum(item.cost() for item in orcamento.budgetproposalitem_set.all())
    return render(request, 'lista_de_orcamentos.html', {'orcamentos': orcamentos})


def generate_budget_pdf(budget_id):
    # Fetch the budget instance
    budget = Orcamento.objects.get(pk=budget_id)

    # Create a PDF document
    filename = f"budget_{budget.pk}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)

    # Styles
    styles = getSampleStyleSheet()
    style_center = ParagraphStyle(name='Center', alignment=1)

    # Content
    content = []

    # Image
    image_path = r"C:\Users\R53\vilma-santos-project\vilma\static\images\1ed09b04-8bdb-42bc-85d0-1fdb00fc6ee8.jpg"
    if image_path:
        img = Image(image_path, width=2*inch, height=1*inch)
        content.append(img)
        content.append(Spacer(1, 0.5*inch))
        content.append(Spacer(1, 0.5*inch))

        # Header
        header_text = Paragraph("<font size='16'><b>Orcamento</b></font>", style_center)
        content.append(header_text)
        content.append(Spacer(1, 0.25 * inch))

        # Table
        table_headers = ['Nome do Produto', 'Quantidade', 'Preco Unitario', 'Valor Final']
        table_data = []
        total_cost = 0

        for item in BudgetProposalItem.objects.filter(proposal=budget):
            product = item.produto
            discounted_price = item.cost()  # Calculate discounted price
            row = [product.nome, item.quantidade, f"€{product.preco:.2f}", f"€{discounted_price:.2f}"]
            if item.desconto > 0:  # Check if discount is greater than 0%
                table_headers.insert(3, 'Desconto')
                row.insert(3, f"{item.desconto}%")
            table_data.append(row)
            total_cost += discounted_price  # Accumulate discounted price for total cost

        table_headers = list(set(table_headers))

        table_data.insert(0, table_headers)  # Insert headers as the first row

        table = Table(table_data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        content.append(table)
        content.append(Spacer(1, 0.25 * inch))

        # Total cost
        total_cost_text = Paragraph(f"<b>Valor total do Orcamento: €{total_cost:.2f}</b>", style_center)
        content.append(total_cost_text)
        content.append(Spacer(1, 1 * inch))

        # Footer
        footer_text = Paragraph("<font size='16'><b>Vilma Santos</b></font>", style_center)
        content.append(footer_text)
        content.append(PageBreak())

        # Build PDF
        doc.build(content)

        return filename

def generate_pdf(request, orcamento_id):
    # Fetch the budget instance
    budget = get_object_or_404(Orcamento, pk=orcamento_id)

    # Generate the PDF
    filename = generate_budget_pdf(budget.id)

    # Serve the PDF as a response
    with open(filename, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


def edit_orcamento(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, pk=orcamento_id)
    BudgetProposalItemFormSet = inlineformset_factory(Orcamento, BudgetProposalItem, fields=('produto', 'quantidade', 'desconto'), extra=1)
    if request.method == 'POST':
        form = OrcamentoForm(request.POST, instance=orcamento)
        formset = BudgetProposalItemFormSet(request.POST, instance=orcamento)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('lista_de_orcamentos')  # Redirect to the orcamentos list page after editing
    else:
        form = OrcamentoForm(instance=orcamento)
        formset = BudgetProposalItemFormSet(instance=orcamento)
    return render(request, 'edit_orcamento.html', {'form': form, 'formset': formset, 'orcamento': orcamento})


def delete_orcamento(request, orcamento_id):
    orcamento = get_object_or_404(Orcamento, pk=orcamento_id)
    if request.method == 'POST':
        orcamento.delete()
        return redirect('lista_de_orcamentos')  # Redirect to the orcamentos list page after deletion
    return render(request, 'delete_orcamento.html', {'orcamento': orcamento})
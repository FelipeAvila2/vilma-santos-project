from django.shortcuts import render, redirect

# Create your views here.
# accounts/views.py

from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.http import JsonResponse

def search_suggestions(request):
    query = request.GET.get('q', '').lower()  # Convert query to lowercase for case-insensitive comparison

    print("Query:", query)  # Print the value of the query for debugging

    if query == "":
        suggestions = ['estoque', 'fornecedores', 'ingredientes', 'ordens de compra']
    else:
        # Define the full list of suggestions
        all_suggestions = ['estoque', 'fornecedores', 'ingredientes', 'ordens de compra']

        # Filter suggestions based on the query
        suggestions = [suggestion for suggestion in all_suggestions if suggestion.lower().startswith(query)]

    print("Suggestions:", suggestions)  # Print the suggestions for debugging

    return JsonResponse({'suggestions': suggestions})


def home(request):
    # Handle search query
    query = request.GET.get('q', '')

    # Define mappings from section names to URL names or paths
    section_mapping = {
        'estoque': 'estoque',  # Replace 'estoque' with the actual URL name or path for the Estoque section
        'fornecedores': 'supplier_list',  # Replace 'supplier_list' with the actual URL name or path for the Suppliers section
        'ingredientes': 'ingredient_list',
        'ordens de compra': 'purchaseorder_list'
        # Add mappings for other sections as needed
    }

    # Get the URL name or path for the requested section
    section_url = section_mapping.get(query)

    # If the query matches a section name, redirect to the corresponding section
    if section_url:
        return redirect(section_url)
    else:
        # Generate URLs for each type of result if no specific section is requested
        estoque_url = reverse('estoque')
        fornecedores_url = reverse('supplier_list')

        # Pass URLs to template
        context = {
            'estoque_url': estoque_url,
            'fornecedores_url': fornecedores_url,
            'query': query,
        }
        return render(request, 'home.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')  # Redirect to the appropriate URL name
        else:
            # Render the login form with errors
            return render(request, 'registration/login.html', {'form': form})
    else:
        # If it's not a POST request, render the login form
        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page




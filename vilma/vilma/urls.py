from django.contrib import admin
from django.urls import path, include
from home import urls as home_urls
from inventorio import urls as inventorio_urls
from producao import urls as producao_urls
from vendas import urls as vendas_urls
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include(home_urls)),
    path('inventorio/', include(inventorio_urls)),
    path('producao/', include(producao_urls)),
    path('vendas/', include(vendas_urls)),
]

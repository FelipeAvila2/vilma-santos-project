from django.urls import path

from .views import home, login_view, logout_view, search_suggestions

urlpatterns = [
    path('', home, name="home"),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('search-suggestions/', search_suggestions, name='search_suggestions')
]

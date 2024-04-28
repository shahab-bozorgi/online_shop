from django.urls import path
from . import views

app_name = 'product'
urlpatterns = [
    path('<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('navbar', views.NavbarView.as_view(), name='navbar'),
    path('all', views.ProductList.as_view(), name='products_list'),
]
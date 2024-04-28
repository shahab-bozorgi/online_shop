

from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView
from product.models import Product, Category, Color


class ProductDetailView(DetailView):
    template_name = 'product/product_detail.html'
    model = Product

class NavbarView(TemplateView):
    template_name = 'includes/navbar.html'

    def get_context_data(self, **kwargs):
        context = super(NavbarView, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context



class ProductList(ListView):
    template_name = 'product/product_list.html'
    queryset = Product.objects.all()
    # context_object_name = 'products'

    def get_context_data(self, **kwargs):
        request = self.request
        colors = request.GET.getlist('color')
        size = request.GET.getlist('size')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        queryset = Product.objects.all()
        if colors:
            queryset = queryset.filter(color__title__in=colors).distinct()


        if size:
            queryset = queryset.filter(size__title__in=size).distinct()

        if min_price and max_price:
            queryset = queryset.filter(price__lte=max_price, price__gte=min_price).distinct()


        # print(colors, size, min_price, max_price)
        context = super(ProductList, self).get_context_data()
        context['object_list'] = queryset
        context['colors'] = Color.objects.all()
        return context



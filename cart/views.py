from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .cart_module import Cart
from django.views.generic import DetailView

from product.models import Product
from .models import Order, OrderItem


class CartDetailView(View):
    def get(self, request):
        cart = Cart(request)
        return render(request, 'cart/cart_detail.html', {'cart': cart})


class CartAddView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, id=pk)
        size, color, quantity = request.POST.get('size', "empty"), request.POST.get('color', "empty"), request.POST.get(
            'quantity')
        cart = Cart(request)
        cart.add(product, size, color, quantity)
        return redirect('cart:cart_detail')


class CartDeleteView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('cart:cart_detail')


class OrderDetailView(View):
    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        return render(request, 'cart/order_detail.html', {'order': order})

class OrderCreationView(View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=int(cart.total()))

        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'], quantity=item['quantity'], color=item['color'],
                                  size=item['size'], price=item['price'])

        return redirect('cart:cart_detail', order.id)

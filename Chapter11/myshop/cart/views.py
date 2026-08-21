from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST

from coupons.forms import CouponApplyForm
from shop.models import Product
from shop.recommender import Recommender

from .cart import Cart
from .forms import CartAddProductForm


def _cart_item(cart, product_id):
    for item in cart:
        if item['product'].id == int(product_id):
            item['update_quantity_form'] = CartAddProductForm(
                initial={'quantity': item['quantity'], 'override': True}
            )
            return item
    return None


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override'],
        )

    if request.htmx:
        item = _cart_item(cart, product_id)
        item_html = render_to_string(
            'cart/detail.html#cart-item', {'item': item}, request=request
        )
        totals_html = render_to_string(
            'cart/detail.html#cart-totals', {'cart': cart}, request=request
        )
        summary_html = render_to_string(
            'shop/cart_summary.html', {'cart': cart}, request=request
        )
        return HttpResponse(item_html + totals_html + summary_html)

    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    if request.htmx:
        return HttpResponse('')

    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'], 'override': True}
        )
    coupon_apply_form = CouponApplyForm()

    r = Recommender()
    cart_products = [item['product'] for item in cart]
    if(cart_products):
        recommended_products = r.suggest_products_for(
            cart_products, max_results=4
        )
    else:
        recommended_products = []

    template_name = "cart/detail.html"
    if request.htmx:
        template_name += "#cart-item"
    return render(
        request,
        template_name,
        {
            'cart': cart,
            'coupon_apply_form': coupon_apply_form,
            'recommended_products': recommended_products
        },
    )

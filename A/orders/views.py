import jdatetime
from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from products.models import Products
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ApplyCouponForm
from .models import Coupon, Order, Cart
from accounts.models import Profile
from permissions import requires_address, AddressIsNotNone, CartIsNotNone
import requests
import json
from django.http import HttpResponse
import datetime

User = get_user_model()


class OrderSummaryView(LoginRequiredMixin, View):
    """ for show information cart
    if user input a code coupon in form
    validate  and true apply
    """

    templates_class = 'orders/summary.html'

    def get(self, request):
        cart = Cart.objects.filter(user=request.user, ordered=False)
        total_price = 0
        if cart:
            # get total price order
            for i in cart:
                total_price += i.price_item()
            return render(request, self.templates_class, {'cart': cart, 'total_price': total_price})
        return render(request, self.templates_class)


class OrderView(LoginRequiredMixin, AddressIsNotNone, CartIsNotNone, View):
    """
    create receipt and apply coupon in order if existed!
    """
    templates_class = 'orders/receipt_coupon.html'
    form_class = ApplyCouponForm

    def setup(self, request, *args, **kwargs):
        self.order = Order.objects.get(user=request.user)

        return super().setup(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.templates_class, {'form': self.form_class, 'order': self.order})

    def post(self, request):
        form = self.form_class(request.POST)
        if not form.data['coupon']:
            # validate form is not empty
            messages.success(request, 'کد تخفیفی وارد نشده است !', 'danger')
            return redirect('orders:order_item')
        if form.is_valid():
            coupon = form.cleaned_data['coupon']
            # check coupon code for exist in database and belong to the user
            try:
                amount = request.user.related_in_coupon.get(code=coupon, is_active=True)
            except:
                if request.user.related_in_coupon.filter(code=coupon, is_active=False):
                    messages.success(request, 'این کد منقضی شده است', 'danger')
                    return redirect('orders:order_item')

                elif Coupon.objects.filter(code=coupon):
                    messages.success(request, 'این کد متعلق به کاربر دیگری میباشد', 'danger')
                    return redirect('orders:order_item')

                messages.success(request, 'کد صحیح نمی باشد !!!', 'danger')
                return redirect('orders:order_item')
                # for validate a coupon and min_order them
            if self.order.all_price < int(amount.min_order):
                messages.success(request, f'حداقل مقدار خرید برای کد تخفیف {amount.min_order} میباشد', 'info')
                return redirect('orders:order_item')

        after_coupon = self.order.all_price - request.user.related_in_coupon.get(code=coupon, is_active=True).amount
        self.order.price_pey = int(after_coupon)
        self.order.price_coupon = int(amount.amount)
        self.order.save()
        messages.success(request,
                         f'کد شما اعمال شد و مبلغ{amount.amount} کم شد مبلغ قابل پرداخت {after_coupon} می باشد',
                         'success')
        return redirect('orders:order_item')


MERCHANT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)

        request.session['order_pay'] = {
            'order_id': order.id,
        }
        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.pay(),
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user, "email": request.user.profile.email}
        }
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session['order_pay']['order_id']

        order = Order.objects.get(id=int(order_id))
        # for edit value quantity product
        for i in order.items.all():
            i.item.quantity = i.item.quantity - i.quantit
        order.save()

        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                          "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.total(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:

                    order.ordered = True
                    order.ordered_date = jdatetime.datetime.now()

                    order.save()
                    return HttpResponse('Transaction success.\nRefID: ' + str(
                        req.json()['data']['ref_id']
                    ))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(
                        req.json()['data']['message']
                    ))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return HttpResponse('Transaction failed or canceled by user')


@login_required
@requires_address
def create_order(request):
    cart = Cart.objects.filter(user=request.user)
    profile = Profile.objects.get(user=request.user)
    order, create = Order.objects.get_or_create(user=request.user)
    order.items.set(cart)
    order.address = profile.address
    order.all_price = order.total()
    order.save()
    return redirect('orders:order_item')


@login_required
def add_to_cart(request, product_slug):
    """add selected product to the cart"""
    product = get_object_or_404(Products, slug=product_slug)
    cart, create = Cart.objects.get_or_create(user=request.user, item=product)

    cart.quantity += 1
    if product.quantity >= cart.quantity:
        # check value quantity is exits
        cart.save()
        messages.success(request, " سبد خرید ویرایش شد.", 'info')
        return redirect('orders:summary_cart')
    else:
        messages.warning(request, 'حداکثر سفارش این محصول به انتها رسیده است', 'danger')
        return redirect('orders:summary_cart')


@login_required
def remove_from_cart(request, product_slug):
    """clear cart from selected product"""
    product = get_object_or_404(Products, slug=product_slug)
    Cart.objects.filter(user=request.user, item=product).delete()
    messages.success(request, "سبد خرید شما پاک شد.", "danger")
    return redirect('orders:summary_cart')


@login_required
def remove_one_cart(request, product_slug):
    # remove one selected product from cart
    product = get_object_or_404(Products, slug=product_slug)
    cart = Cart.objects.get(user=request.user, item=product)
    if cart.quantity == 1:
        # check if quantity product is 1 ,delete a product from cart and show another message
        Cart.objects.filter(user=request.user, item=product).delete()
        messages.success(request, "سبد خرید شما پاک شد.", "danger")
        return redirect('orders:summary_cart')
    cart.quantity -= 1
    cart.save()
    messages.success(request, " سبد خرید ویرایش شد.", "warning")
    return redirect('orders:summary_cart')

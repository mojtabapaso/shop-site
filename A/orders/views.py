from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from products.models import Products
from .models import Cart, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ApplyCouponForm, AddressForm
from .models import Coupon, Address


class OrderView(View):
    pass


class OrderSummaryView(LoginRequiredMixin, View):
    """ for show information cart

    if user input a code coupon in form
    validate  and true apply
    """

    templates_class = 'orders/summary.html'
    total_price = 0

    def get(self, request):

        cart = Cart.objects.filter(user=request.user, ordered=False)
        if cart:
            # this if and value submitted , just for show in HTML !
            for object in cart:
                self.total_price += object.item.price * object.quantity

            return render(request, self.templates_class,
                          {'cart': cart, 'total_price': self.total_price})

        return render(request, self.templates_class, {'cart': cart})


class ApplyCouponView(LoginRequiredMixin, View):
    templates_class = 'orders/summary.html'
    from_class = ApplyCouponForm

    def post(self, request):
        form = self.from_class(request.POST)

        if not form.data['coupon']:
            # validate form is not empty
            messages.success(request, 'کد تخفیفی وارد نشده است !', 'danger')
            return redirect('orders:last_step')

        if form.is_valid():
            coupon = form.cleaned_data['coupon']
            # check coupon code for exist in database and belong to the user
            try:
                request.user.related_in_coupon.get(code=coupon, is_active=True)


            except:
                if Coupon.objects.filter(code=coupon, is_active=False):
                    messages.success(request, 'این کد منقضی شده است', 'danger')
                    return redirect('orders:last_step')
                elif Coupon.objects.filter(code=coupon):
                    messages.success(request, 'این کد متعلق به کاربر دیگری میباشد', 'danger')
                    return redirect('orders:last_step')
                messages.success(request, 'کد صحیح نمی باشد !!!', 'danger')
                return redirect('orders:last_step')

        messages.success(request, 'کد شما اعمال شد', 'success')

        return redirect('orders:last_step')


class LastStepView(LoginRequiredMixin, View):
    from_class = ApplyCouponForm
    form_address = AddressForm

    templates = 'orders/last_step.html'

    def get(self, request):
        address = Address.objects.filter(user=request.user)
        print(request.user.address_user)
        print("|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||")
        for i in address:
            print(i.address)

        print(request.user.address_user)
        return render(request, self.templates,
                      {'form': self.from_class, 'form_address': self.form_address, 'address': address})

    def post(self, request):
        form = self.form_address(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            Address.objects.create(user=request.user, address=cd['address'])
            messages.success(request, 'go to pay', 'info')
            return redirect('orders:last_step')
        messages.error(request, 'rid', 'danger')
        return redirect('pages:home')


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

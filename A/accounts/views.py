from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyCodeForm
from .models import User
from random import randint
from jalali_date import datetime2jalali, date2jalali
from .models import OtpCode
from utils import send_otp_code


class RegisterView(View):
    form_class = UserRegisterForm
    templates_class = 'accounts/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.templates_class, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = randint(10000, 99999)
            send_otp_code = (form.cleaned_data['phone_number'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
            cd = form.cleaned_data
            request.session['user_registered_info'] = {'phone_number': cd['phone_number'],
                                                       'email': cd['email_form'],
                                                       'first_name': cd['first_name'],
                                                       'last_name': cd['last_name'],
                                                       'date_of_birth': cd['date_of_birth'],
                                                       'password': cd['password']}
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')

        return render(request, self.templates_class, {'form': form})


class VerifyCodeView(View):
    form_class = VerifyCodeForm
    templates_class = 'accounts/verify.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.templates_class, {'form': form})

    def post(self):
        pass


class LoginView(View):
    pass


class LogoutView(View):
    pass

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, VerifyCodeForm, UserLoginForm
from .models import User
from random import randint
from jalali_date import datetime2jalali, date2jalali
from .models import OtpCode
from utils import send_otp_code
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin


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
                                                       'date_of_birth': cd['date_of_birth'].strftime('%Y-%m-%d'),
                                                       'password': cd['password']}
            messages.success(request, 'we sent you a code', 'success')
            return redirect('accounts:verify_code')

        return render(request, self.templates_class, {'form': form})


class VerifyCodeRegisterView(View):
    form_class = VerifyCodeForm
    templates_class = 'accounts/verify.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.templates_class, {'form': form})

    def post(self, request):
        user_sessions = request.session['user_registered_info']
        code_instance = OtpCode.objects.get(phone_number=user_sessions['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            if form.cleaned_data['code'] == code_instance.code:
                User.objects.create_user(email=user_sessions['email'], phone_number=user_sessions['phone_number'],
                                         first_name=user_sessions['first_name'], last_name=user_sessions['last_name'],
                                         date_of_birth=user_sessions['date_of_birth'],
                                         password=user_sessions['password'])
                code_instance.delete()
                messages.success(request, 'OK ', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'Not Math code', 'error')
                return redirect('accounts:verify_code')
        return render(request, self.templates_class, {'form': form})


class LoginView(View):
    form_class = UserLoginForm
    template_class = 'accounts/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_class, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone_number'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'OK', 'success')
                return redirect('home:home')
            messages.error(request, "Not Good Man", 'error')
        return render(request, self.template_class, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "OK Good boy", 'success')
        return redirect('home:home')

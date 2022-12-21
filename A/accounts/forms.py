from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.messages.context_processors import messages
from django.core.exceptions import ValidationError
from .models import User
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'first_name', 'last_name',)
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change your password  using <a href=\"../password/\">this form</a>")

    class Meta:
        model = User
        fields = (
            'email', 'phone_number', 'last_name', 'first_name', 'password', 'date_of_birth', 'is_active', 'is_admin',)


class UserRegisterForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    email_form = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'special'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField()
    date_of_birth = forms.DateField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['date_of_birth'] = JalaliDateField(label=('date_of_birth'), widget=AdminJalaliDateWidget)

    def clean_number_phone(self):
        phone_number = self.cleaned_data['phone_number']
        if User.objects.filter(phone_number=self.phone_number).exists():
            raise ValidationError('this number phone already exists !!!')
        return phone_number

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=self.email).exists():
            raise ValidationError('this email already exists !!!')
        return email


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserLoginForm(forms.Form):
    phone_number = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ChangePasswordForm(forms.Form):
    new_password1 = forms.CharField(widget=forms.PasswordInput())
    new_password_confirm = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        if self.new_password1 and self.new_password_confirm and self.new_password1 != self.new_password_confirm:
            return messages ('password be must mach')

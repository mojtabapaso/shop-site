from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django_jalali.db import models as jmodels
from .managers import UserManager


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_admin = models.BooleanField(default=False, verbose_name="مدیر")
    last_login = jmodels.jDateTimeField(blank=True, null=True, verbose_name='آخرین بازدید')
    objects = UserManager()
    USERNAME_FIELD = 'phone_number'

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.phone_number} - {self.code} '

    class Meta:
        verbose_name = "کد ارسالی"
        verbose_name_plural = 'کدهای ارسالی'


class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='profile')
    date_of_berth = models.CharField(max_length=12, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    address = models.TextField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f'{self.user}'

    class Meta:
        verbose_name = "پروفایل"
        verbose_name_plural = 'پروفایل ها'

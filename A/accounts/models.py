from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django_jalali.db import models as jmodels
from .managers import UserManager


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, max_length=250, verbose_name="ایمیل")
    phone_number = models.CharField(max_length=11, unique=True, verbose_name="شماره تلفن")
    first_name = models.CharField(max_length=150, verbose_name="اسم")
    last_name = models.CharField(max_length=150, verbose_name="فامیلی")
    date_of_birth = jmodels.jDateField(verbose_name='تاریخ تولد', null=True)
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    is_admin = models.BooleanField(default=False, verbose_name="مدیر")
    last_login = jmodels.jDateTimeField(blank=True, null=True, verbose_name='آخرین بازدید')
    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'date_of_birth', ]

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.email

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

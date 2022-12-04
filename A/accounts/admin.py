from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserChangeForm, UserCreationForm
from .models import User, OtpCode
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('first_name', 'last_name', 'phone_number', 'email', 'date_of_birth', 'is_admin')
    list_filter = ()
    # ##('date', JDateFieldListFilter,), ('datetime', JDateFieldListFilter,),
    fieldsets = ((None, {'fields': ('first_name', 'last_name', 'phone_number', 'email', 'password')}),
                 ('Personal info', {'fields': ('date_of_birth',)}),
                 ('Permissions', {'fields': ('is_admin', 'last_login')}),)
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'date_of_birth', 'password1', 'password2'), }),)
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    readonly_fields = ('last_login',)


admin.site.register(User, UserAdmin)


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


admin.site.unregister(Group)

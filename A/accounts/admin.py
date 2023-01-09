from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .forms import UserChangeForm, UserCreationForm
from .models import User, OtpCode ,Profile
from django_jalali.admin.filters import JDateFieldListFilter
import django_jalali.admin as jadmin


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('phone_number', 'is_admin')
    list_filter = ()
    # ##('date', JDateFieldListFilter,), ('datetime', JDateFieldListFilter,),
    fieldsets = (
    (None, {'fields': ('phone_number', 'password')}), ('Permissions', {'fields': ('is_admin', 'last_login')}))
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('password1', 'password2'), }),)
    search_fields = ('phone_number',)
    ordering = ('phone_number',)
    filter_horizontal = ()
    readonly_fields = ('last_login',)


admin.site.register(User, UserAdmin)

admin.site.register(Profile)

@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created')


admin.site.unregister(Group)

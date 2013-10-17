from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.utils.translation import ugettext_lazy as _

from .models import User
from .forms import UserCreationForm, UserChangeForm


class UserAdmin(AuthUserAdmin):

    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'password1',
                       'password2',)},),
    )
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        'first_name', 'last_name', 'email', 'is_active',
        'is_staff']
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('first_name', 'last_name', 'email')

admin.site.register(User, UserAdmin)

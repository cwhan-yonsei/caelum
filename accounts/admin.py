from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreationForm, UserChangeForm, AdminUserChangeForm
from .models import User

# Register your models here.
class UserAdmin(BaseUserAdmin):
    form = AdminUserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'name', 'dept_major')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'portal_id', 'name', 'dept_major', 'username',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin', 'is_email_verified',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
            }
        )
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
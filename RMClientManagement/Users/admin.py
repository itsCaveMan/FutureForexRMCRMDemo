from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from . import models


class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
            (
                None,
                {'fields': ('email', 'username', 'password')}
            ),
            ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'email_confirmed', 'user_role', 'groups', 'user_permissions', 'primary_rm')}),
            ('Important dates', {'fields': ('last_login', 'created_on')}),
    )
    limited_fieldsets = (
            (
                None,
                {'fields': ('email', 'username',)}
            ),
            ('Important dates', {'fields': ('last_login', 'created_on_utc')}),
    )
    add_fieldsets = (
            (
                None,
                {'classes': ('wide',), 'fields': ('email', 'username', 'password1', 'password2')}
            ),
    )

    change_password_form = auth_admin.AdminPasswordChangeForm
    list_display = ('email', 'is_superuser', )
    list_filter = ( 'is_superuser', 'is_active', 'is_staff', 'groups', 'user_role',)
    search_fields = ['email']
    ordering = ('-created_on_utc',)
    readonly_fields = ('last_login', 'created_on_utc',)



admin.site.register(models.User, UserAdmin)
admin.site.register(models.UserProfile)

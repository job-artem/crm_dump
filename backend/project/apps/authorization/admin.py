from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import User

admin.site.unregister(Group)


@register(User)
class UserAdmin(UserAdmin):
    ordering = ['email']
    fieldsets = (
        ('Базовая информация:', {'fields': ('email', 'password')}),
        ('Личная информация:', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Параметры аккаунта:', {'fields': ['user_type']}),
        ('Раздел для аккаунта тренера:', {'fields': ['user_group']}),
        ('Файлы пользователя:', {'fields': ['image']}),
        ('Посещаемость;', {'fields': ('last_login', 'date_joined', 'update_at')}),

    )
    readonly_fields = ('last_login', 'date_joined', 'update_at')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'user_type', 'last_login')
    model = User

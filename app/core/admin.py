from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name', 'user_type']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'biography')}),
        (
            _('Permission'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'user_type')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Advertisement)
admin.site.register(models.Classroom)
admin.site.register(models.Tutorial)
admin.site.register(models.Comment)
admin.site.register(models.Tag)
admin.site.register(models.DirectMessage)
admin.site.register(models.Question)
admin.site.register(models.QuestionChoice)
admin.site.register(models.QuestionAnswer)
admin.site.register(models.Chat)


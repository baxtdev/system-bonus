from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from django.forms import TextInput, Textarea, NumberInput
from django.db import models
from django import forms

from easy_maps.widgets import AddressWithMapWidget

from .models import User,Notification

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'20'})},
        models.IntegerField: {'widget': NumberInput(attrs={'size':'20'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }
    list_display = (
        'phone',
        'first_name',
        'last_name',
        'email',
        'code',
        'bonus',
        'get_online_status',
    )
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'code')
    filter_horizontal = ('groups', 'user_permissions')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'sex')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': (
            'image',
            'phone',
            'password',
        )}),
        (_('Personal info'), {'fields': (
            'first_name',
            'last_name',
            'email',
            'birthday',
            'sex',
            'address',
        )}),
        (_('Карта'), {'fields': (
            'code',
            'bonus',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        (_('Important dates'), {'fields': (
            'date_joined',
            'last_login',
            'last_activity',
        )}),
    )
    readonly_fields = (
        'code',
        'bonus',
        'date_joined',
        'last_activity',
        'last_login'
    )
    # autocomplete_fields = (
    #     'address',
    # )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2'),
        }),
    )

    def get_online_status(self, user):
        return user.online

    get_online_status.boolean = True
    get_online_status.short_description = _('online')
    class form(forms.ModelForm):
        class Meta:
            widgets = {
                'address': AddressWithMapWidget({'class': 'vTextField'})
            }



@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    pass
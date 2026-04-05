from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Device, User


@admin.register(User)
class CubiUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'created_at', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Cubi', {'fields': ('role', 'created_at')}),
    )
    readonly_fields = ('created_at',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_id', 'owner', 'device_name', 'association_code')

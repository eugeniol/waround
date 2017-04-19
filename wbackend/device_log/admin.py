from django.contrib import admin
from device_log import models



class DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac_address', 'customer', 'friendly_name')

admin.site.register(models.Device , DeviceAdmin)

class DeviceLogAdmin(admin.ModelAdmin):
    list_display = ('device', 'created_at', 'type')
    readonly_fields = ('created_at',)

admin.site.register(models.DeviceLog, DeviceLogAdmin)

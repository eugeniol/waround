from django.contrib import admin
from device_log import models

admin.site.register(models.Device)
admin.site.register(models.DeviceLog)

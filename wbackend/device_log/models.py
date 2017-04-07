from django.contrib.auth.models import User
from django.db import models

from customers.models import Customer

class Device(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True)
    public_id = models.CharField(max_length=255, unique=True)
    friendly_name = models.CharField(max_length=255, blank=True)
    mac_address = models.CharField(max_length=255)

    def __str__(self):
        return self.friendly_name + ' (' + self.mac_address + ')'


class DeviceLog(models.Model):
    device = models.ForeignKey(Device)
    LOG_ACTION = (
        (0, 'IN'),
        (1, 'OUT'),
    )
    type = models.IntegerField(default=0, choices=LOG_ACTION)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.device.__str__() + ' ' + self.created_at.isoformat() + ' ' + DeviceLog.LOG_ACTION[self.type][1]

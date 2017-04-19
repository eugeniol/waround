from django.contrib.auth.models import User
from django.db import models

from customers.models import Customer


class Device(models.Model):
    customer = models.ForeignKey(Customer, null=True, blank=True)
    public_id = models.CharField(max_length=255, unique=True)
    friendly_name = models.CharField(max_length=255, blank=True)
    mac_address = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True)

    def __unicode__(self):
        if self.customer:
            return self.customer.__unicode__() + ' - ' + self.friendly_name + ' (' + self.mac_address + ')'
        elif self.friendly_name and self.mac_address:
            return self.friendly_name + ' (' + self.mac_address + ')'
        else:
            return self.public_id


class DeviceLog(models.Model):
    device = models.ForeignKey(Device)
    LOG_ACTION = (
        (0, 'IN'),
        (1, 'OUT'),
    )
    type = models.IntegerField(default=0, choices=LOG_ACTION)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        if (self.device):
            return self.device.__unicode__() + ' ' + self.created_at.isoformat() + ' ' + \
                   DeviceLog.LOG_ACTION[self.type][1]
        else:
            return self.created_at.isoformat() + ' ' + DeviceLog.LOG_ACTION[self.type][1]

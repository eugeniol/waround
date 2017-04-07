from django.contrib.auth.models import User
from rest_framework import serializers
from device_log import models


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ('first_name', 'last_name')


class DeviceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required=False, allow_null=True)
    class Meta:
        model = models.Device
        fields = ('id', 'public_id', 'customer', 'friendly_name', 'mac_address')


class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DeviceLog
        fields = ('id', 'device', 'created_at', 'type')


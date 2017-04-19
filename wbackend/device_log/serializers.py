from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from device_log import models

from device_log.models import DeviceLog


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Customer
        fields = ('first_name', 'last_name')


class DeviceSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(required=False, allow_null=True, read_only=True)

    class Meta:
        model = models.Device
        fields = ('id', 'public_id', 'customer', 'friendly_name', 'mac_address')


class DeviceLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceLog
        fields = ('id', 'device', 'created_at', 'type')

    def create(self, validated_data):
        existent = None
        try:
            existent = DeviceLog.objects.filter(device=validated_data['device']).order_by('-created_at')[0:1].get()
        except(ObjectDoesNotExist):
            pass

        if existent is None or existent.type != validated_data['type']:
            return DeviceLog.objects.create(**validated_data)
        else:
            return existent

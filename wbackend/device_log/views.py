from rest_auth import serializers
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework import serializers
from rest_framework import generics
from device_log.models import Device, DeviceLog
from device_log.serializers import DeviceLogSerializer, DeviceSerializer, CustomerSerializer

import django_filters.rest_framework


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = Device.objects.all()
        public_id = self.request.query_params.get('public_id', None)
        if public_id is not None:
            queryset = queryset.filter(public_id=public_id)

        return queryset


import django_filters.rest_framework


class DeviceLogViewSet(viewsets.ModelViewSet):
    queryset = DeviceLog.objects.all()
    serializer_class = DeviceLogSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        queryset = DeviceLog.objects.all()

        public_id = self.request.query_params.get('device', None)

        if public_id is not None:
            queryset = queryset.filter(device=public_id)

        queryset = queryset.order_by('-created_at')

        return queryset

# class BaseViewSet(viewsets.ModelViewSet):
# authentication_classes = (SessionAuthentication, TokenAuthentication, BasicAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#
# class AlumnoViewSet(BaseViewSet):
#     # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
#     queryset = Alumno.objects.all()
#     serializer_class = AlumnoSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_fields = ('user__id', 'curso', 'curso__nivel')
#
#
# class NivelViewSet(BaseViewSet):
#     queryset = Nivel.objects.all()
#     serializer_class = NivelSerializer
#
#
# class CursoViewSet(BaseViewSet):
#     queryset = Curso.objects.all()
#     serializer_class = CursoSerializer
#     filter_backends = (filters.DjangoFilterBackend,)
#     filter_fields = ('ciclo', 'ciclo__activo',)
#
#
# from rest_framework import generics
#
#
# class MateriaNombreSerializer(serializers.ModelSerializer):
#     nombre = serializers.StringRelatedField(source='nombre.nombre')
#
#     class Meta:
#         model = Materia
#         fields = ('id', 'nombre')
#
#
# class DocenteSerializer(serializers.ModelSerializer):
#     user = UserSimpleSerializer()
#
#     class Meta:
#         model = Docente
#         fields = ('id', 'tipo', 'user')
#
#
# class CursoMateriaFullSerializer(serializers.ModelSerializer):
#     docentes = DocenteSerializer(many=True)
#     materia = MateriaNombreSerializer()
#
#     class Meta:
#         model = CursoMateria
#         fields = ('id', 'materia', 'docentes')
#
#
# class FullCursoSerializer(CursoSerializer):
#     nivel = NivelSerializer()
#     materias = CursoMateriaFullSerializer(many=True)
#
#     class Meta:
#         model = Curso
#         fields = ('id', 'ciclo', 'nivel', 'materias')
#
#
# class AlumnoCursoSerializer(AlumnoSerializer):
#     curso = FullCursoSerializer()
#
# from rest_framework import  mixins
#
# class AlumnoCursosViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
#     queryset = Alumno.objects.all()
#     serializer_class = AlumnoCursoSerializer
#     authentication_classes = (SessionAuthentication, TokenAuthentication)
#     permission_classes = (IsAuthenticated,)
#
#     def get_queryset(self):
#         """
#         This view should return a list of all the purchases
#         for the currently authenticated user.
#         """
#         user = self.request.user
#         return Alumno.objects.filter(user=user)

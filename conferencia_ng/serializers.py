from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['us_nombres','us_apellidos','us_dni', 'us_telefono', 
                  'us_zone', 'us_imagen_pago']

class AsistenciaZonaSerializer(serializers.Serializer):
    us_zone = serializers.CharField()
    total_inscritos = serializers.IntegerField()
    asistentes_dia1 = serializers.IntegerField()
    asistentes_dia2 = serializers.IntegerField()

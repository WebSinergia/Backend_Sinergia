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
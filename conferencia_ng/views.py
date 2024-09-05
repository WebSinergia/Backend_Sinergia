import qrcode
import os

from django.conf import settings
from django.shortcuts import render
from django.core.files import File
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework import generics, exceptions, status
from rest_framework.response import Response

from cryptography.fernet import Fernet
from io import BytesIO

from .models import User
from .serializers import *

SECRET_KEY = b'xN_1zj_Eprrk6DAq6ibY8tkhLc3vb5HPMMyBPAxP0Oc='

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.all().order_by('us_nombres')
    
class UserRetrieveDNIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        dni = self.request.query_params.get('dni')
        return User.objects.filter(us_dni=dni).first()

class UserRetrieveIDView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_object(self):
        id = self.request.query_params.get('id')
        return User.objects.filter(us_id=id).first()
    
class UserUpdatePaymentView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'us_id'

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        
        user.us_pago_confirmado = True
        user.save()

        serializer = self.get_serializer(user)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class UserGetImageByZoneView(generics.ListAPIView):
    def get(self, request, zone_id):
        
        zone_data = {
            1: {"name": "Luisa Calderón Urrunaga", "celular": "991478475", "modalidad": "YAPE"},
            2: {"name": "Caleb Reategui Cevallos", "celular": "945073269", "modalidad": "YAPE"},
            4: {"name": "Katherin Rengifo Silva", "celular": "990075683", "modalidad": "YAPE"},
            5: {"name": "Elias Josue Ojeda Cerdan", "celular": "9974312513", "modalidad": "YAPE/PLIN"},
            6: {"name": "Gina Retuerto Guadalupe", "celular": "907745120", "modalidad": "YAPE"},
            7: {"name": "Charly Chavez Rosas", "celular": "931714774", "modalidad": "YAPE"},
            8: {"name": "Carmen Espejo Arredondo", "celular": "966716579", "modalidad": "YAPE"},
            9: {"name": "Jesely Torres Ramirez", "celular": "997033170", "modalidad": "YAPE"},
            10: {"name": "Ashley Jimenez Arroyo", "celular": "959190013", "modalidad": "YAPE"},
            11: {"name": "Marcos Espinoza Ojanama", "celular": "981283678", "modalidad": "YAPE/PLIN"},
            12: {"name": "Domenick Romero Pariona", "celular": "983650627", "modalidad": "YAPE"},
            13: {"name": "Sandy Bravo Cordova", "celular": "914549354", "modalidad": "YAPE"},
            14: {"name": "Daniel Velasquez Gavelan", "celular": "952119186", "modalidad": "YAPE"},
            15: {"name": "Gabriel Aron Ortiz Alfaro", "celular": "902412431", "modalidad": "YAPE"},
            16: {"name": "Frank Ramos Victorio", "celular": "946896936", "modalidad": "YAPE"},
        }
        
        # Construir el nombre del archivo de imagen
        image_file = f'zona{zone_id}.png'
        image_path = os.path.join(settings.MEDIA_ROOT, 'zone-images', image_file)

        # Verificar si la imagen existe
        if os.path.exists(image_path):
            # Construir la URL completa de la imagen
            image_url = request.build_absolute_uri(f'{settings.MEDIA_URL}zone-images/{image_file}')
            
            # Obtener los datos de la zona si existen
            if zone_id in zone_data:
                data = zone_data[zone_id]
                data['image_url'] = image_url
            else:
                data = {'image_url': image_url}
            return Response(data)
        else:
            raise Http404("Imagen no encontrada")
    
class UserRetrieveAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    cipher = Fernet(SECRET_KEY)
    
    def get_object(self):
        # Extraer el ID encriptado de los parámetros de la URL
        encrypted_id = self.request.query_params.get('id')
        
        # Decodificar el ID encriptado
        decrypted_id = self.cipher.decrypt(encrypted_id.encode()).decode()

        # Buscar el objeto `User` usando el ID decodificado
        return generics.get_object_or_404(User, pk=decrypted_id)
    
class UserCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        generate_qr_and_encrypt_id(user)
        user.save()
    
def generate_qr_and_encrypt_id(user):
    cipher = Fernet(SECRET_KEY)

    # Encriptar el ID del usuario
    encrypted_id = cipher.encrypt(str(user.us_id).encode())

    # Definir la URL del frontend para la redireccion a la pagina web de marcado de asistencia
    base_url = "https://nuevasgeneraciones.netlify.app/asistencia"
    data = f"{base_url}?id={user.us_id}"

    # Generar el QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Convertir el QR a un archivo de imagen
    img = qr.make_image(fill='black', back_color='white')
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_image = File(buffer, name=f"{user.us_nombres}_qr.png")

    # Asignar la imagen del QR al usuario y guardar
    user.us_qrcode.save(f"{user.us_nombres}_qr.png", qr_image)

import django
import qrcode
import os
from django.conf import settings
from conferencia_ng.models import User

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'conferencia.settings')
django.setup()

# Directorio donde se guardarán los códigos QR
QR_CODES_DIR = os.path.join(settings.MEDIA_ROOT, 'qr_codes')

# Asegúrate de que el directorio existe
os.makedirs(QR_CODES_DIR, exist_ok=True)    

def generate_qr_code(user_id):
    # Generar la URL correcta con el ID del usuario
    qr_url = f"https://nuevasgeneraciones.netlify.app/asistencia?id={user_id}"
    
    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_url)
    qr.make(fit=True)
    
    
    # Crear la imagen del QR
    img = qr.make_image(fill='black', back_color='white')
    
    # Nombre del archivo QR
    qr_filename = f'qr_{user_id}.png'
    qr_path = os.path.join(QR_CODES_DIR, qr_filename)
    
    # Guardar el código QR en el directorio
    img.save(qr_path)
    
    # Retornar la ruta relativa al archivo en la carpeta media/qr-codes
    qr_access_url = f"qr_codes/{qr_filename}"
    return qr_access_url


def regenerate_qr_codes():
    for user in User.objects.all():
        # Generar el código QR y obtener la nueva URL
        new_qr_url = generate_qr_code(user.us_id)
        
        # Actualizar la URL del QR en la base de datos
        user.us_qrcode = new_qr_url
        user.save()

# Llama a esta función para regenerar todos los QR
regenerate_qr_codes()

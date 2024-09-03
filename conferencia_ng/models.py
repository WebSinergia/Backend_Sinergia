from django.db import models

# Create your models here.
class User(models.Model):
    
    #-------CAMPOS OBLIGATORIOS--------#
    us_id = models.SmallAutoField(primary_key=True)
    us_nombres = models.CharField(max_length=100)
    us_apellidos = models.CharField(max_length=100)
    us_dni = models.CharField(max_length=10)
    us_telefono = models.CharField(max_length=10)
    us_zone = models.CharField(max_length=100)
    us_lugar = models.CharField(max_length=100)
    
    #-------BOOLEANO--------#
    us_pago_confirmado = models.BooleanField(default=False)
    
    #-------IMAGENES--------#
    us_imagen_pago = models.ImageField(upload_to='payment_images/', null=True, blank=True)
    us_qrcode = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def __str__(self):
        return self.nombre

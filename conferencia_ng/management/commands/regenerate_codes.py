from django.core.management.base import BaseCommand
from conferencia_ng.models import User
from conferencia_ng import generate_codes

class Command(BaseCommand):
    help = 'Regenera los códigos QR para todos los usuarios'

    def handle(self, *args, **kwargs):
        generate_codes()
        self.stdout.write(self.style.SUCCESS('Códigos QR regenerados exitosamente.'))

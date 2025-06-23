from django.core.management.base import BaseCommand
from plume_app.services import fetch_and_save_plume_data

class Command(BaseCommand):
    help = 'Fetch and save Plume analytics data'
    
    def handle(self, *args, **options):
        if fetch_and_save_plume_data():
            self.stdout.write(self.style.SUCCESS('Datos de Plume guardados correctamente'))
        else:
            self.stdout.write(self.style.ERROR('Error al guardar los datos'))
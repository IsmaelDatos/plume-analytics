from django.core.management.base import BaseCommand
from plume_app.services import get_battle_groups
from django.core.cache import cache
from django.conf import settings

class Command(BaseCommand):
    help = "Pre-carga todos los Battle Groups en caché para mejorar el rendimiento"

    def handle(self, *args, **options):
        try:
            groups = get_battle_groups(max_requests=10)  # Ajusta según necesidad
            cache.set('all_battle_groups', groups, timeout=3600)  # Cache por 1 hora
            self.stdout.write(self.style.SUCCESS('✅ Battle Groups precargados en caché'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error: {str(e)}'))
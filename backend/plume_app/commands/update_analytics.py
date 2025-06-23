from django.core.management.base import BaseCommand
from plume_app.analytics_service import PlumeAnalyticsService

class Command(BaseCommand):
    help = 'Updates the global analytics data'
    
    def handle(self, *args, **options):
        analyzer = PlumeAnalyticsService()
        results = analyzer.analyze_leaderboard()
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully updated analytics data. Total XP: {results['summary']['total_xp']:,}")
        )
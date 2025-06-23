from celery import shared_task
from plume_app.analytics_service import PlumeAnalyticsService
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_analytics_daily():
    try:
        logger.info("Iniciando actualización diaria de analytics")
        analyzer = PlumeAnalyticsService()
        result = analyzer.analyze_leaderboard()
        logger.info(f"Actualización completada: {result}")
        return "OK"
    except Exception as e:
        logger.error(f"Error en actualización diaria: {str(e)}")
        raise
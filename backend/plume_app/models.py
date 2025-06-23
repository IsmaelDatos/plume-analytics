from django.db import models

class AnalyticsSnapshot(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    total_xp = models.BigIntegerField()
    total_wallets = models.IntegerField()
    plume_per_xp = models.FloatField()
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"Snapshot {self.timestamp.strftime('%Y-%m-%d %H:%M')} - {self.total_xp:,} XP"
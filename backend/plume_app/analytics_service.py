import requests
import time
from typing import Dict, List, Tuple
from .models import AnalyticsSnapshot
from django.utils import timezone

class PlumeAnalyticsService:
    BASE_URL = "https://portal-api.plume.org/api/v1/stats/leaderboard"
    
    def __init__(self):
        self.total_xp = 0
        self.total_wallets = 0
        self.max_xp = 0
        self.min_xp = float('inf')
        self.all_wallets_data = []
        self.PLUME_S2_ALLOCATION = 152_000_000
        self.plume_per_xp = 0

    def fetch_leaderboard_data(self, offset: int, count: int) -> Tuple[List[Dict], bool]:
        params = {
            'offset': offset,
            'count': count,
            'walletAddress': 'undefined',
            'overrideDay1Override': 'false',
            'preview': 'false'
        }
        
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get('data', {}).get('leaderboard', []), True
        except Exception:
            return [], False

    def analyze_leaderboard(self, max_offset=177904, batch_size=5000):
        current_offset = 0
        
        while current_offset <= max_offset:
            count = min(batch_size, max_offset - current_offset + 1)
            data, success = self.fetch_leaderboard_data(current_offset, count)
            
            if not success or not data:
                break
                
            for wallet in data:
                xp = wallet.get('totalXp', 0)
                self.total_xp += xp
                self.total_wallets += 1
                self.max_xp = max(self.max_xp, xp)
                self.min_xp = min(self.min_xp, xp)
                self.all_wallets_data.append(wallet)
                
            current_offset += count
            time.sleep(0.1)  # Rate limiting
            
        if self.total_xp > 0:
            self.plume_per_xp = self.PLUME_S2_ALLOCATION / self.total_xp
            
        # Save snapshot to database
        snapshot = AnalyticsSnapshot.objects.create(
            total_xp=self.total_xp,
            total_wallets=self.total_wallets,
            plume_per_xp=self.plume_per_xp
        )
        
        return self.get_analysis_results()

    def get_tiers_analysis(self):
        tiers = [
            (0, 999, "Tier 1: 0-999 XP"),
            (1000, 1999, "Tier 2: 1K-2K XP"),
            (2000, 2999, "Tier 3: 2K-3K XP"),
            (3000, 3999, "Tier 4: 3K-4K XP"),
            (4000, 4999, "Tier 5: 4K-5K XP"),
            (5000, 9999, "Tier 6: 5K-10K XP"),
            (10000, 19999, "Tier 7: 10K-20K XP"),
            (20000, 29999, "Tier 8: 20K-30K XP"),
            (30000, 39999, "Tier 9: 30K-40K XP"),
            (40000, 49999, "Tier 10: 40K-50K XP"),
            (50000, self.max_xp, f"Tier 11: 50K+ XP")
        ]
        
        analysis = []
        for tier_min, tier_max, tier_name in tiers:
            tier_wallets = [w for w in self.all_wallets_data 
                          if tier_min <= w.get('totalXp', 0) <= tier_max]
            
            if not tier_wallets:
                continue
                
            tier_xp = sum(w.get('totalXp', 0) for w in tier_wallets)
            tier_plume = tier_xp * self.plume_per_xp
            
            analysis.append({
                'name': tier_name,
                'wallet_count': len(tier_wallets),
                'percentage': (len(tier_wallets) / self.total_wallets) * 100,
                'total_xp': tier_xp,
                'total_plume': tier_plume,
                'avg_xp': tier_xp / len(tier_wallets)
            })
            
        return analysis

    def get_analysis_results(self):
        avg_xp = self.total_xp / self.total_wallets if self.total_wallets > 0 else 0
        
        return {
            'summary': {
                'total_xp': self.total_xp,
                'total_wallets': self.total_wallets,
                'average_xp': avg_xp,
                'max_xp': self.max_xp,
                'min_xp': self.min_xp,
                'plume_per_xp': self.plume_per_xp,
                'plume_s2_allocation': self.PLUME_S2_ALLOCATION,
                'timestamp': timezone.now()
            },
            'tiers': self.get_tiers_analysis(),
            'historical': self.get_historical_data()
        }

    def get_historical_data(self):
        snapshots = AnalyticsSnapshot.objects.all().order_by('timestamp')[:30]  # Last 30 snapshots
        return {
            'dates': [s.timestamp.strftime('%Y-%m-%d') for s in snapshots],
            'total_xp': [s.total_xp for s in snapshots],
            'total_wallets': [s.total_wallets for s in snapshots]
        }
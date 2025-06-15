import requests
from django.conf import settings

PLUME_API_BASE = "https://portal-api.plume.org/api/v1"

def get_leaderboard(offset=0, count=20):
    url = f"{PLUME_API_BASE}/stats/leaderboard"
    params = {
        'offset': offset,
        'count': count,
        'walletAddress': 'undefined',
        'overrideDay1Override': 'false',
        'preview': 'false'
    }
    response = requests.get(url, params=params)
    return response.json().get('data', {}).get('leaderboard', [])

def get_wallet_stats(wallet_address):
    url = f"{PLUME_API_BASE}/stats/wallet"
    params = {'walletAddress': wallet_address}
    response = requests.get(url, params=params)
    return response.json().get('data', {})

def get_wallet_badges(wallet_address):
    url = f"{PLUME_API_BASE}/badges"
    params = {'walletAddress': wallet_address}
    response = requests.get(url, params=params)
    return response.json().get('data', {}).get('badges', [])

def get_social_connections(wallet_address):
    url = f"{PLUME_API_BASE}/user/social-connections"
    params = {'walletAddress': wallet_address}
    response = requests.get(url, params=params)
    return response.json().get('data', {})

def get_daily_spin_data(wallet_address):
    url = f"{PLUME_API_BASE}/stats/dailySpinData"
    params = {'walletAddress': wallet_address}
    response = requests.get(url, params=params)
    return response.json().get('data', {}).get('spinHistory', [])

def get_all_apps():
    url = f"{PLUME_API_BASE}/apps"
    response = requests.get(url)
    return response.json().get('data', {}).get('apps', [])
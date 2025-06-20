import requests
from django.conf import settings
import time  

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
    """
    Obtiene estadísticas de la wallet desde la API de Plume
    Args:
        wallet_address (str): Dirección de la wallet (0x...)
    Returns:
        dict: Respuesta JSON de la API
    """
    url = f"https://portal-api.plume.org/api/v1/stats/wallet"
    headers = {
        'Accept': 'application/json',
        'User-Agent': 'PlumeAnalytics/1.0'
    }
    params = {
        'walletAddress': wallet_address,
        '_': int(time.time())  # Evita caché
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Lanza error para respuestas 4XX/5XX
        return response.json()
        
    except requests.exceptions.RequestException:
        return {'data': {}}  # Devuelve estructura vacía si hay error

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

def get_battle_groups(max_requests=1000):
    """Obtiene todos los battle groups con sus wallets de forma optimizada"""
    all_wallets = []
    offset = 0
    count = 5000
    requests_made = 0
    
    while requests_made < max_requests:
        try:
            leaderboard = get_leaderboard(offset=offset, count=count)
            if not leaderboard:
                break  
            all_wallets.extend(leaderboard)
            offset += count
            requests_made += 1
            if len(leaderboard) < count:
                break
        except Exception as e:
            print(f"Error fetching leaderboard (offset {offset}): {e}")
            break
    battle_groups = {}
    for wallet in all_wallets:
        bg = wallet.get('battleGroup')
        if bg:
            if bg not in battle_groups:
                battle_groups[bg] = []
            battle_groups[bg].append(wallet)
    return battle_groups
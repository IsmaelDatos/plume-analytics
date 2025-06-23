from django.shortcuts import render, redirect
from django.contrib import messages
from .analytics_service import PlumeAnalyticsService
from django.utils import timezone
from .services import (
    get_leaderboard,
    get_wallet_stats,
    get_wallet_badges,
    get_social_connections,
    get_daily_spin_data,
    get_all_apps,
    get_battle_groups
)
import requests

def home(request):
    try:
        leaderboard = get_leaderboard(offset=0, count=20)
        return render(request, 'plume_app/home.html', {
            'leaderboard': leaderboard
        })
    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error connecting to Plume API: {str(e)}")
        return render(request, 'plume_app/home.html', {'leaderboard': []})

def wallet_detail(request, wallet_address):
    try:
        # Obtener datos de la API
        api_response = get_wallet_stats(wallet_address)
        data = api_response.get('data', {})
        stats = data.get('stats', {})
        
        # Manejo robusto de seasonOneAllocation
        season_one = data.get('seasonOneAllocation')
        airdrop_claim = season_one.get('airdropClaim', {}) if season_one else {}

        # Construir contexto
        context = {
            'stats': stats,
            'wallet_badges': get_wallet_badges(wallet_address),
            'social_connections': get_social_connections(wallet_address),
            'daily_spins': get_daily_spin_data(wallet_address),
            'wallet_address': wallet_address,
            'has_season_data': season_one is not None,  # Flag para la plantilla
            'season_one': {
                'base_allocation': season_one.get('calculatedAllocation') if season_one else None,
                'boost': season_one.get('calculatedBoost') if season_one else None,
                'total_airdrop': season_one.get('calculatedTotal') if season_one else None,
                'quests_completed': airdrop_claim.get('questBonusActivatedCount'),
                'initial_claim': airdrop_claim.get('initialClaimAmountTokens')
            }
        }
        return render(request, 'plume_app/wallet_detail.html', context)

    except Exception as e:
        print(f"Error loading wallet {wallet_address}: {str(e)}")
        messages.error(request, "Could not load wallet data. Please try again later.")
        return render(request, 'plume_app/wallet_detail.html', {
            'wallet_address': wallet_address,
            'error': True
        })

def wallet_search(request):
    search_address = request.GET.get('wallet_address', '').strip()
    if search_address and len(search_address) == 42 and search_address.startswith('0x'):
        return redirect('wallet_detail', wallet_address=search_address)
    else:
        messages.error(request, "Please enter a valid Ethereum address (42 characters starting with 0x)")
        return redirect('home')
    
def leaderboard(request):
    offset = int(request.GET.get('offset', 0))
    count = int(request.GET.get('count', 100))
    
    try:
        leaderboard_data = get_leaderboard(offset=offset, count=count)
        
        return render(request, 'plume_app/leaderboard.html', {
            'leaderboard': leaderboard_data,
            'current_offset': offset,
            'count': count
        })
    except Exception as e:
        messages.error(request, f"Error loading leaderboard: {str(e)}")
        return redirect('home')

def compare_wallets(request):
    wallet1 = request.GET.get('wallet1')
    wallet2 = request.GET.get('wallet2')
    
    context = {
        'wallet1': wallet1,
        'wallet2': wallet2
    }
    
    if wallet1:
        try:
            context['wallet1_data'] = {
                'stats': get_wallet_stats(wallet1),
                'badges': get_wallet_badges(wallet1),
                'social': get_social_connections(wallet1)
            }
        except Exception as e:
            context['wallet1_error'] = str(e)
    
    if wallet2:
        try:
            context['wallet2_data'] = {
                'stats': get_wallet_stats(wallet2),
                'badges': get_wallet_badges(wallet2),
                'social': get_social_connections(wallet2)
            }
        except Exception as e:
            context['wallet2_error'] = str(e)
    
    return render(request, 'plume_app/compare.html', context)

def battle_groups(request):
    try:
        messages.info(request, "Loading battle groups data... This may take a moment.")
        battle_groups_data = get_battle_groups(max_requests=1000) 
        if not battle_groups_data:
            messages.warning(request, "No battle groups data could be loaded. Please try again later.")
            return redirect('home')
        sorted_groups = sorted(
            battle_groups_data.items(),
            key=lambda x: x[0] if x[0] is not None else float('inf')
        )
        storage = messages.get_messages(request)
        for _ in storage:
            pass  
        return render(request, 'plume_app/battle_groups.html', {
            'battle_groups': dict(sorted_groups)
        })
    except Exception as e:
        messages.error(request, f"Error loading battle groups: {str(e)}")
        return redirect('home')
    
def global_analytics(request):
    analyzer = PlumeAnalyticsService()
    
    # Opción para forzar actualización
    refresh = request.GET.get('refresh', 'false').lower() == 'true'
    
    if refresh:
        data = analyzer.analyze_leaderboard()
    else:
        # Mostrar los últimos datos disponibles
        data = analyzer.get_analysis_results()
    
    return render(request, 'plume_app/analytics.html', {
        'data': data,
        'last_updated': timezone.now()
    })
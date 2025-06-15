from django.shortcuts import render, redirect
from django.contrib import messages
from .services import (
    get_leaderboard,
    get_wallet_stats,
    get_wallet_badges,
    get_social_connections,
    get_daily_spin_data,
    get_all_apps
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
        response = get_wallet_stats(wallet_address)
        
        # Acceso correcto a los datos anidados
        stats = response.get('data', {}).get('stats', {})
        season_one = response.get('data', {}).get('seasonOneAllocation', {})
        
        context = {
            'stats': stats,
            'wallet_badges': get_wallet_badges(wallet_address),
            'social_connections': get_social_connections(wallet_address),
            'daily_spins': get_daily_spin_data(wallet_address),
            'wallet_address': wallet_address,
            'season_one': {
                'base_allocation': season_one.get('calculatedAllocation', 0),
                'boost': season_one.get('calculatedBoost', 0),
                'total_airdrop': season_one.get('calculatedTotal', 0),
                'quests_completed': season_one.get('questBonusActivatedCount', 0),
                'initial_claim': season_one.get('airdropClaim', {}).get('initialClaimAmountTokens', 0)
            }
        }
        return render(request, 'plume_app/wallet_detail.html', context)
    except Exception as e:
        messages.error(request, f"Error loading wallet: {str(e)}")
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

    search_address = request.GET.get('wallet_address')
    if search_address:
        return redirect('wallet_detail', wallet_address=search_address)
    else:
        messages.error(request, "Please enter a valid wallet address")
        return redirect('home')
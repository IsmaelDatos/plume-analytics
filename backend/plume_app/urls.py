from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('wallet/', views.wallet_search, name='wallet_search'),
    path('wallet/<str:wallet_address>/', views.wallet_detail, name='wallet_detail'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('compare/', views.compare_wallets, name='compare_wallets'),
    path('battle-groups/', views.battle_groups, name='battle_groups'),
    path('analytics/', views.global_analytics, name='global_analytics'),
]
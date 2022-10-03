from django.urls import path
from api.v1.wallet.views import *

app_name = 'wallet'

urlpatterns = [
    path('info', info_wallet, name='info-wallet'),
    path('info-super', info_wallet_super, name='info-wallet-super'),
    path('transfer', transfer_to_wallet, name='transfer-to-wallet'),
    path('confirm-transfer', confirm_transfer_to_wallet, name='transfer-to-wallet'),
    path('withdraw', withdraw_from_wallet, name='withdraw-from-wallet'),
    path('confirm-withdraw', confirm_withdraw, name='withdraw-from-wallet'),
    path('history', history_wallet, name='history-of-wallet'),
    path('history-super', history_wallet_super, name='history-of-wallet-super'),
    path('transaction-history', transactions_history_view, name='history-of-transactions'),
    path('card', CardListView.as_view(), name='card-list'),
    path('card/<int:pk>', CardDetailView.as_view(), name='card-detail'),
    path('create-wallet', create_wallet, name='create-wallet'),
]
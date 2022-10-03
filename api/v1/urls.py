from django.urls import path, include

urlpatterns = [
    path('accounts/', include('api.v1.account.urls')),
    # path('courses/', include('api.v1.courses.urls')),
    # path('orders/', include('api.v1.orders.urls')),
    path('wallet/', include('api.v1.wallet.urls')),
]
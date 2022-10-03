from django.urls import path
from api.v1.ad.views import *

app_name = 'ad'

urlpatterns = [
    path('create-ad/', create_ad, name='create-ad'),
    path('update-ad/<int:pk>', update_ad, name='update-ad'),
    path('delete-ad/<int:pk>', delete_ad, name='delete-ad'),
    path('get-ad/<int:pk>', get_ad, name='get-ad'),
    path('get-ads/', ads_view, name='get-ads'),

]
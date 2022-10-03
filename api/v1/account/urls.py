from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView

from api.v1.account.views import *

app_name = 'accounts'

urlpatterns = [
    path('step-one/', step_one, name='step-one'),
    path('step-two/', step_two, name='step-two'),
    path('register', registration_view, name='registration'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    ]
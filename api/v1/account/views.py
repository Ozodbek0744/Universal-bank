import random
import requests
from decouple import config
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from urllib.error import HTTPError
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.models.otp import Otp
from accounts.models.account import Account
from api.v1.account.serializers import *

SMS_AUTH_TOKEN = config('SMS_AUTH_TOKEN')
SMS_URL = config('SMS_URL')


@swagger_auto_schema(method="post", tags=["accounts"], request_body=OtpSerializer)
@api_view(['POST'])
def step_one(request):
    if request.method == 'POST':

        header = {'Authorization': 'Bearer ' + SMS_AUTH_TOKEN}

        request_data = request.data
        sms_code = str(random.randint(10000, 99999))

        data = {
            'mobile_phone': f'{request_data["mobile"]}',
            'message': f'{sms_code}',
            'from': '4546',
            'callback_url': 'http://0000.uz/test.php'
        }

        try:
            r = requests.post(SMS_URL, json=data, headers=header)
        except HTTPError:
            raise Http404

        enc_otp = pbkdf2_sha256.encrypt(sms_code, rounds=12000, salt_size=32)

        serializer_data = {
            'mobile': request_data['mobile'],
            'otp': sms_code,
            'enc_otp': enc_otp,
        }

        otp_code = Otp(mobile=request_data['mobile'])
        serializer = OtpSerializer(otp_code, data=serializer_data)
        data = {}

        if serializer.is_valid():
            serializer.save()
            data = {
                'success': "Successfully sent and added",
                'otp_generated': enc_otp,
                'sms_service_response': r.json(),
            }
            return Response(data=data, status=status.HTTP_201_CREATED)
        return Response(r.json())


@swagger_auto_schema(method="post", tags=["accounts"], request_body=StepTwoSerializer)
@api_view(['POST'])
def step_two(request):
    if request.method == 'POST':
        data = request.data
        context = {}
        try:
            mobile_user = Otp.objects.get(enc_otp=data['otp_token'])
        except:
            return Response({'status': False, 'message': 'This token has not been found.'})

        if not mobile_user.is_active:
            return Response({'status': False, 'message': 'This token has been expired!'})

        if pbkdf2_sha256.verify(data['otp'], mobile_user.enc_otp):
            try:
                user = Account.objects.get(phone_number=mobile_user.mobile)
            except:
                return Response({'status': True, 'message': 'This user should be registered!'})

            refresh = RefreshToken.for_user(user)
            context['jwt_token'] = {
                'status': True,
                'message': 'This user had been registered before',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(context)
        else:
            return Response({'status': False, 'message': 'The code is not correct'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'status': True, 'message': 'Code verified!'}, status=status.HTTP_200_OK)


@swagger_auto_schema(method="post", tags=["accounts"], request_body=RegistrationSerializer)
@api_view(['POST', ])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered a new user."
            data['phone_number'] = account.phone_number
            refresh = RefreshToken.for_user(account)
            data['jwt_token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        else:
            data = serializer.errors
        return Response(data)

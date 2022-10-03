from re import A
import requests
from decouple import config
from django.conf import settings
from django.db.utils import IntegrityError
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import *
from api.v1.ad.serializers import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, RetrieveAPIView


@swagger_auto_schema(method="post", tags=["Ad"], request_body=AdSerializer)
@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def create_ad(request):
    user = request.user
    ad = AdModel(owner=user)
    serializer = AdSerializer(ad, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method="put", tags=["Ad"], request_body=AdSerializer)
@api_view(['PUT'])
@permission_classes((IsAuthenticated,))
def update_ad(request, pk):
    user =request.user
    try:
        ad = AdModel.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if ad.owner != user:
        return Response(status=status.HTTP_403_FORBIDDEN)
        
    serializer = AdSerializer(ad, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
@swagger_auto_schema(method="delete", tags=["Ad"], request_body=AdSerializer)
@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def delete_ad(request, pk):
    user =request.user

    try:
        ad = AdModel.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if ad.owner != user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    try:
        ad.delete()
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(status=status.HTTP_304_NOT_MODIFIED)


@swagger_auto_schema(method="get", tags=["Ad"])
@api_view(['GET'])
def get_ad(request, pk):
    try:
        ad = AdModel.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = AdSerializer(ad)
    return Response(serializer.data, status=status.HTTP_200_OK)



@swagger_auto_schema(method="get", tags=["Ad"])
@api_view(['GET',])
def ads_view(request):
    paginator = PageNumberPagination()
    paginator.page_size = 10
    person_objects = AdModel.objects.all()
    result_page = paginator.paginate_queryset(person_objects, request)
    serializer = AdSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)
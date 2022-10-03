from dataclasses import fields
from rest_framework import serializers
from app.models import *
from api.v1.account.serializers import CountrySerializer

class AdPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdPicturModel
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
# class CreateAdSerializer(serializers.ModelSerializer):
    picture = AdPictureSerializer()
    country = CountrySerializer()

    class Meta:
        model = AdModel
        fields = ['price', 'picture','country','state', 'color', 'quantity', 'model', 'comment', 'ram', 'memory', 'dicount_price']
    
class FavSerializer(serializers.ModelSerializer):

    class Meta:
        model = FavAdModel
        fields = '__all__'
from abc import ABC

from rest_framework import serializers
# from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from wallet.models import CardModel, VoucherModel, TransferModel


class WalletSuperSerializer(serializers.Serializer):
    wallet_number = serializers.CharField(required=True, allow_blank=True, max_length=100)
    expire = serializers.CharField(required=True, allow_blank=True, max_length=100)


class CreateWalletSerializer(serializers.Serializer):
    number = serializers.CharField(required=True, max_length=25)


class TransferSerializer(serializers.Serializer):
    number = serializers.CharField(required=True, allow_blank=True, max_length=100)
    expire = serializers.CharField(required=True, allow_blank=True, max_length=100)
    amount = serializers.IntegerField(required=True)
    is_saved_card = serializers.BooleanField(required=True)

    def validate(self, data):
        if data['amount'] < 100:
            raise serializers.ValidationError("Amount should be more than or equal 100 sums")
        return data


class ConfirmTransferSerializer(serializers.Serializer):
    tr_id = serializers.CharField(required=True, allow_blank=False, max_length=100)
    code = serializers.CharField(required=False, allow_blank=True, max_length=100)


class ConfirmWithdrawSerializer(serializers.Serializer):
    tr_id = serializers.CharField(required=True, allow_blank=False, max_length=100)


class WalletHistorySerializer(serializers.Serializer):
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)


class WalletHistorySuperSerializer(serializers.Serializer):
    card_number = serializers.CharField(required=True, allow_blank=True, max_length=100)
    expire = serializers.CharField(required=True, allow_blank=True, max_length=100)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)



class CardAddSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_username_from_owner')

    class Meta:
        model = CardModel
        fields = [
            'card_number',
            'expire',
            'owner'
        ]

    def get_username_from_owner(self, card):
        owner = card.owner.phone_number
        return owner


class CardSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField('get_username_from_owner')
    card_number = serializers.SerializerMethodField('get_card_number')

    class Meta:
        model = CardModel
        fields = [
            'card_number',
            'card_uuid',
            'expire',
            'owner'
        ]

    def get_username_from_owner(self, card):
        owner = card.owner.phone_number
        return owner

    def get_card_number(self, card):
        try:
            card_number = f"{card.card_number[:4]}********{card.card_number[-4:]}"
        except:
            card_number = card.card_number
        return card_number


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferModel
        fields = '__all__'
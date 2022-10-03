from dataclasses import fields
from accounts.models.account import Account
from accounts.models.country import CountryModel
from rest_framework import serializers
from accounts.models.otp import Otp


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryModel
        fields = '__all__'



class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = Account
        fields = [
            'phone_number',
            'password',
            'password2',
            'f_name',
            'l_name',
            'sex'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        account = Account(
            phone_number=self.validated_data['phone_number'],
            f_name=self.validated_data['f_name'],
            l_name=self.validated_data['l_name'],
            sex=self.validated_data['sex'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Password must match!'})
        account.set_password(password)
        account.save()
        return account



class AccountSerializer(serializers.ModelSerializer):
    f_name = serializers.SerializerMethodField('get_f_name_method')
    l_name = serializers.SerializerMethodField('get_l_name_method')
    country = CountrySerializer()

    class Meta:
        model = Account
        exclude = ["is_admin", "is_staff", "is_superuser"]

    def get_f_name_method(self, obj):
        if obj.f_name is None or obj.f_name is False:
            f_name = ''
        else:
            f_name = obj.f_name
        return f_name

    def get_l_name_method(self, obj):
        if obj.l_name is None or obj.l_name is False:
            l_name = ''
        else:
            l_name = obj.l_name
        return l_name

class OtpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Otp
        fields = '__all__'

class StepTwoSerializer(serializers.Serializer):
    otp_token = serializers.CharField(max_length=255)
    otp = serializers.CharField(max_length=255)

    class Meta:
        fields = '__all__'

# class AccountPropertiesSerializers(serializers.ModelSerializer):

#     class Meta:
#         model = Account
#         fields = [
#             'f_name',
#             'l_name',
#             'email',
#             'sex',
#             'date_birth',
#             'country',
#             'district',
#             'speciality',
#             'profile_picture',
#             'interests',
#             'about_me',
#             'is_speaker'
#         ]


# class BecomeSpeakerSerializers(serializers.ModelSerializer):

#     class Meta:
#         model = Account
#         fields = ['is_speaker']


# class DeactivateAccountSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Account
#         fields = ['is_active']

#     def update(self, instance, validated_data):
#         instance.is_admin = False
#         instance.is_active = False
#         instance.is_staff = False
#         instance.is_superuser = False
#         instance.is_superuser = False
#         instance.save()
#         return instance








# class ForgotPasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = Account
#         fields = ('password', 'password2')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})

#         return attrs

#     def update(self, instance, validated_data):

#         instance.set_password(validated_data['password'])
#         instance.save()

#         return instance


# class ChangePasswordSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)
#     old_password = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = Account
#         fields = ('old_password', 'password', 'password2')

#     def validate(self, attrs):
#         if attrs['password'] != attrs['password2']:
#             raise serializers.ValidationError({"password": "Password fields didn't match."})

#         return attrs

#     def validate_old_password(self, value):
#         print(self.context)
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError({"old_password": "Old password is not correct"})
#         return value

#     def update(self, instance, validated_data):

#         instance.set_password(validated_data['password'])
#         instance.save()

#         return instance


# class DevicesSerializer(serializers.ModelSerializer):
#     username = serializers.SerializerMethodField('get_username_from_author')

#     class Meta:
#         model = DeviceModel
#         fields = [
#             'device_name',
#             'ip',
#             'os',
#             'browser',
#             'imei',
#             'mac',
#             'name',
#             'lat',
#             'long',
#             'firebase_reg_id',
#             'uuid',
#             'username'
#         ]

#     def get_username_from_author(self, device):
#         username = device.owner.phone_number
#         return username
from importlib import import_module
from django.shortcuts import render
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from uuid import uuid4
from wallet.services import create_wallet_util
from ads.models import FavAdModel
from .country import CountryModel
from wallet.models import WalletModel

def upload_location(instance, filename):
    ext = filename.split('.')[-1]
    file_path = 'accounts/avatars/{user_id}-{phone_number}'.format(
        user_id=str(instance.id), phone_number='{}.{}'.format(uuid4().hex, ext))
    return file_path
    

class MyAccountManage(BaseUserManager):
    def create_user(self, f_name,  phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have number')

        user = self.model(
            phone_number=phone_number,
            f_name=f_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, f_name, phone_number, password):
        user = self.create_user(
            f_name=f_name,
            password=password,
            phone_number=phone_number,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True)
    f_name = models.CharField(max_length=50, blank=True, null=True)
    l_name = models.CharField(max_length=50, blank=True, null=True)
    sex = models.BooleanField(null=True, blank=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to=upload_location, null=True, blank=True)
    country = models.ForeignKey(CountryModel, on_delete=models.SET_NULL, null=True, blank=True)
    wallet = models.ForeignKey(WalletModel, on_delete=models.SET_NULL, null=True, blank=True)
    favs = models.ForeignKey(FavAdModel, on_delete=models.SET_NULL, null=True, blank=True)


    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['f_name']

    objects = MyAccountManage()

    def str(self):
        return str(self.phone_number)

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        app_label = 'accounts'

    @property
    def profile_picture_url(self):
        try:
            image_url = str(self.profile_picture)
        except:
            image_url = ''

        return image_url


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_wallet(sender, instance=None, created=False, **kwargs):
    if created:
        data = create_wallet_util(instance.phone_number)
        print(f"***************************\ndata_inside_db: {data}\n****************************************")
        card_number = data['result']['card_number']
        expire = data['result']['expire']

        WalletModel.objects.create(
            owner=instance,
            card_number=card_number,
            expire=expire,
        )
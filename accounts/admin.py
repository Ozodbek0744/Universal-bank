from django.contrib import admin
from accounts.models.account import Account
from accounts.models.country import CountryModel
admin.site.register(Account)
admin.site.register(CountryModel)
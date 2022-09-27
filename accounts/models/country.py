from django.db import models

class CountryModel(models.Model):
    region = models.CharField(max_length=255, blank=True, null=True)
    distict = models.CharField(max_length=255, blank=True, null=True)


    def __str__(self):
        return str(self.name)

    class Meta:
        app_label = "accounts"
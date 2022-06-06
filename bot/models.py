from django.db import models
import telegram


class Profile(models.Model):

    first_name = models.CharField(max_length=125, null=True, blank=True)
    last_name = models.CharField(max_length=125, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    telegram_id = models.CharField(max_length=125, null=True)
    
    def __str__(self):
        return self.first_name


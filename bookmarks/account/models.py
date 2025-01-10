from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # The one-to-one field user will be used to associate profiles with users
    # using AUTH_USER_MODEL allows you to customize or replace the user model with your own implementation,
    # making your code more flexible and reusable.
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


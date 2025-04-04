from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # The one-to-one field user will be used to associate profiles with users
    # using AUTH_USER_MODEL allows you to customize or replace the user model with your own implementation,
    # making your code more flexible and reusable.
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


# Intermediate model to build relationship between users.
#
# When a user follows another (user_follow view):
# A Contact record is created (user_from=request.user, user_to=target_user).
# An Action is logged ("X is following Y").
# The following field (dynamically added to User) allows:
#
# user.following.all() → Users this user follows.
#
# user.followers.all() → Users following this user.
class Contact(models.Model):
    # The user who initiates the follow
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_from_set',
        on_delete=models.CASCADE
    )
    # The user being followed
    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='rel_to_set',
        on_delete=models.CASCADE
    )
    # When the follow relationship was established
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['-created'])]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# Add the following field to User dynamically
# add_to_class(name, value): A method that adds an attribute to an existing class after it's been defined.
user_model = get_user_model()
# Gets the active User model with get_user_model() (which might be Django's built-in User or a custom one)
user_model.add_to_class(
    'following',
    models.ManyToManyField(
        'self',
        through=Contact,
        related_name='followers',
        symmetrical=False
        # Indicates that the relationship is directional(if I follow you, it doesn’t mean that you automatically follow me).
    )
)
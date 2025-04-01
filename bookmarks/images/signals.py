from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Image


@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()

# @receiver:
# A decorator provided by Django to connect a function (the signal handler) to a signal.
# It lets Django know which function to call when the signal is emitted.

# m2m_changed:
# Specifies that this function should be called whenever there is a change in a Many-to-Many field.

# Image.users_like.through references that intermediate model.

# instance:
# The instance of the Image model whose users_like field has changed. This is the image for which likes have been added or removed.
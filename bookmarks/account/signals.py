from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_from_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# The post_save signal is a built-in Django signal that is sent after a model’s save() method completes.
#
# In the decorator, we specify the sender as settings.AUTH_USER_MODEL, which ensures that this signal receiver only
# listens for the post_save signal emitted by the User model. When the signal is fired, Django passes several
# arguments to the connected function, including:
#
# sender: The model class that sent the signal (here, the User model).
#
# instance: The actual instance of the User that was just saved.

# Including sender in the function definition allows you to access or check which model triggered the signal. This is
# particularly useful when the same signal handler could potentially listen to signals from multiple models.

# The created parameter is a boolean flag automatically provided by Django in the post_save signal. It indicates
# whether the save() method created a new record (True) or updated an existing one (False).
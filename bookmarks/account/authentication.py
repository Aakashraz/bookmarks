from django.contrib.auth.models import User
from .models import Profile


class EmailAuthBackend:
    """
    Authenticate users using email.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                # This method handles the password hashing
                # to compare the given password with the password stored in the database
                return user
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            # The DoesNotExist exception is raised if no user is found with the given email address. The
            # MultipleObjectsReturned exception is raised if multiple users are found with the same email
            # address
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def create_profile(backend, user, *args, **kwargs):
    """
    Create a user profile for social authentication
    """
    Profile.objects.get_or_create(user=user)
# This function takes two required arguments:
# backend: The social auth backend used for user authentication. Remember that you added
# the social authentication backends to the AUTHENTICATION_BACKENDS setting in your project.
# user: The User instance of the new or existing authenticated user.

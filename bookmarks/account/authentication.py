from django.contrib.auth.models import User


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


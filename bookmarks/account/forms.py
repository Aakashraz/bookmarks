from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'email']

    # This method is executed when the form is validated by calling its is_valid() method.
    # You can provide a clean_<fieldname>() method to any
    # of your form fields to clean the value or raise form validation errors for a specific field.
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match.")
        return cd['password2']

    def clean_email(self):
        cd = self.cleaned_data['email']
        if User.objects.filter(email=cd).exists():
            raise forms.ValidationError("Email already exists.")
        return cd


# This will allow users to edit their first name, last name, and email, which are
# attributes of the built-in Django user model.
class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def clean_email(self):
        cd = self.cleaned_data['email']
        # Query the database for any users with this email, excluding the current user
        qs = User.objects.exclude(
            id=self.instance.id     # prevents the current user from being counted in this check
        ).filter(email=cd)          # looks for users with the submitted email
        if qs.exists():
            raise forms.ValidationError("Email already in use.")
        return cd       # if we get here, the email is unique, so return it


# This will allow users to edit the profile data that is saved in the custom Profile model.
# Users will be able to edit their date of birth and upload an image for their profile picture.
class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']

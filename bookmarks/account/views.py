from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
            # Note the difference between authenticate() and login(): authenticate() verifies the
            # user’s credentials and, upon validation, returns a User object representing the authenticated user.
            # In contrast, login() sets the user in the current session by incorporating the
            # authenticated User object into the current session context.
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard'}
    )


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # For security reasons, instead of saving the raw
            # password entered by the user, we use the set_password() method of the user model. This method
            # handles password hashing before storing the password in the database.
            new_user.save()

            # Create the user Profile
            Profile.objects.create(user=new_user)
            # When users register on the site, a corresponding Profile object will be automatically created and
            # associated with the User object created. However, users created through the administration site won’t
            # automatically get an associated Profile object
            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user}
                          )
    else:
        user_form = UserRegistrationForm()

    return render(request,
                  'account/register.html',
                  {'user_form': user_form}
                  )


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        # instance=request.user: Pre-fills the form with the currently logged-in user's data.
        # data=request.POST: Populates the form with submitted data from the POST request to
        # update the user’s information.
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        # instance=request.user.profile: Pre-fills the form with data from the user's profile.
        # data=request.POST: Populates the form with submitted data from the POST request to update profile fields.
        # files=request.FILES: Includes any files (e.g., profile pictures) uploaded via the form.

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Error updating profile')
        # return redirect('dashboard')
    else:
        user_form = UserEditForm(instance=request.user)  # This shows the user their current data in the form fields.
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(request,
                  'account/edit.html',
                  {
                      'user_form': user_form,
                      'profile_form': profile_form
                  }
                  )


User = get_user_model()

# The user_list view gets all active users.
@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    return render(
        request,
        'account/user/list.html',
        {'section': 'people', 'users': users}
    )


@login_required
def user_detail(request, username):
    # to retrieve the active user with the given username.
    user = get_object_or_404(User, username=username, is_active=True)
    return render(
        request,
        'account/user/detail.html',
        {'section': 'people', 'user': user}
    )
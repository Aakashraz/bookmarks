from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile, Contact
from django.contrib import messages
from django.views.decorators.http import require_POST

from actions.utils import create_action
from actions.models import Action

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
    # Display all actions by default
    actions = Action.objects.exclude(user=request.user)

    following_ids = request.user.following.values_list(
        'id', flat=True
    )
    # when the code does request.user.following.values_list('id', flat=True), it's:
    # Accessing the current user's "following" relationship
    # Retrieving just the IDs of those followed users
    # Getting them as a flat list (like [1, 5, 9]) rather than tuples (which would look like [(1,), (5,), (9,)])

    if following_ids:
        # If user is following others, retrieve only their actions
        actions = actions.filter(user_id__in=following_ids)

    # This restricts the results to just first 10 actions.
    # select_related('user', 'user__profile') → Reduces database hits for User and Profile.
    # prefetch_related('target') → Efficiently loads generic foreign key targets (e.g., posts, images).
    actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    # The 'user__profile' part uses Django's double underscore notation to "traverse" relationships:
    # 'user' tells Django to follow the foreign key from Action to User
    # 'user__profile' tells Django to then follow the relationship from User to Profile
    # It's like saying: "Start at Action, go to its User, then go to that User's Profile."
    #
    # We don't use order_by() in the QuerySet because we rely on the default ordering provided in the Meta options
    # of the Action model. Recent actions will come first since we set ordering = ['-created'] in the Action model.

    return render(
        request,
        'account/dashboard.html',
        {'section': 'dashboard', 'actions': actions}
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
            # Profile.objects.create(user=new_user)
            # When users register on the site, a corresponding Profile object will be automatically created and
            # associated with the User object created. However, users created through the administration site won’t
            # automatically get an associated Profile object

            create_action(new_user, 'has create an account')
            # After a new user account is created and the associated profile is saved, the action has created
            # an account is logged. This captures the event of a new user registration.

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

# Adding user follow/unfollow actions with JavaScript
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            # Prevent the user from following themselves.
            if user == request.user:
                return JsonResponse({'status': 'error', 'message': 'You cannot follow yourself.'})

            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
                # When a user follows another user, the relationship is created (or removed, in the case of
                # unfollowing). In the case of following, the action is following is logged to record that the
                # current user has started following someone else

            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status':'error'})
    return JsonResponse({'status':'error'})
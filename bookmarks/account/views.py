from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm


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

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm


@login_required
def image_create(request):
    print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")

    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        # data=request.POST - populates the form with the submitted data from POST request
        if form.is_valid():
            # form data is validx
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            print(f"Before saving: User = {request.user}, Authenticated = {request.user.is_authenticated}")
            if request.user.is_authenticated:
                # assign current user to the item. This is how we will know who uploaded each image.
                new_image.user = request.user
                new_image.save()
            messages.success(request, 'Image was successfully added')
            # redirect to new created item detail view
            return redirect(new_image.get_absolute_url())
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(
        request,
        'images/image/create.html',
        {'section': 'images', 'form': form}
    )

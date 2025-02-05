from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image


@login_required
def image_create(request):
    print(f"User: {request.user}, Authenticated: {request.user.is_authenticated}")

    if request.method == 'POST':
        # form is sent
        form = ImageCreateForm(data=request.POST)
        # data=request.POST - populates the form with the submitted data from POST request
        if form.is_valid():
            # form data is valid
            try:
                new_image = form.save(commit=False)
                print(f"Before saving: User = {request.user}, Authenticated = {request.user.is_authenticated}")
                print(f"Before user assignment: Image ID={new_image.id}, User={getattr(new_image, 'user', None)}")
                # assign current user to the item. This is how we will know who uploaded each image.
                new_image.user = request.user
                print(f"After user assignment: Image ID={new_image.id}, User={new_image.user}")
                new_image.save()
                print(f"After SAVE: Image ID={new_image.id}, User={new_image.user}")
                messages.success(request, 'Image was successfully added')
                # redirect to new created item detail view
                return redirect(new_image.get_absolute_url())
            except Exception as e:
                print(f"Error saving image: {str(e)}")
                messages.error(request, f"Error saving image: {str(e)}")
                raise
    else:
        # build form with data provided by the bookmarklet via GET
        form = ImageCreateForm(data=request.GET)
    return render(
        request,
        'images/image/create.html',
        {'section': 'images', 'form': form}
    )


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image/detail.html',
                  {'section': 'images', 'image': image}
                  )

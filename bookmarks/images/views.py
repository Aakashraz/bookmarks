from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template import TemplateDoesNotExist
from django.template.loader import get_template

from .forms import ImageCreateForm
from .models import Image

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse


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


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            # This line adds the currently logged-in user (request.user) to the users_like set of the image object.
            # This establishes a relationship in the database that this user now "likes" this image.
            else:
                image.users_like.remove(request.user)
            # When a user clicks an "unlike" button (or toggles from "like" to "unlike"), this line removes the
            # currently logged-in user (request.user) from the users_like set of the image. This breaks the
            # relationship, indicating the user no longer "likes" the image.
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    # to debug the template don't exist error
    # try:
    #     get_template('images/image/list_images.html')
    #     print("Template list_images found!")
    #     get_template('images/image/list.html')
    #     print("Template list found!")
    # except TemplateDoesNotExist as e:
    #     print(f"Template error: {e}")

    images = Image.objects.all()
    paginator = Paginator(images, 6)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    try:
        images = paginator.page(page)
    #   Alternatively can also be used the below code:
    #   images = paginator.get_page(page)

    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            # If AJAX request and page out of range return an empty page
            return HttpResponse('')
        # If page out of range return last page of results
        images = paginator.page(paginator.num_pages)
    if images_only:
        return render(
            request,
            'images/image/list_images.html',
            {'section': 'images', 'images': images}
        )
    return render(
        request,'images/image/list.html',{'section': 'images', 'images': images}
    )

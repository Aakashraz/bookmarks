from django import forms
from .models import Image
import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets= {
            'url': forms.HiddenInput,   # this field will not be visible to users
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.rsplit('.', 1)[1].lower()
        # The rsplit() method splits the URL from the right side on the last dot to get the file extension.
        # For example, "http://example.com/photo.jpg" becomes "jpg".
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url

    # overriding the save() of the ModelForm
    def save(self, force_insert=False, force_update=False, commit=True):
        # it creates an image object but doesn't save it to the database yet
        image = super().save(commit=False)

        # processes the image URL and creates a filename
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.rsplit('.', 1)[1].lower()
        image_name = f'{name}.{extension}'

        #  The Requests Python library is used to download the image by sending an HTTP GET request
        # using the image URL. The response is stored in the response object.
        # The requests.get() downloads the image content, and ContentFile wraps the binary content
        # so Django can save it as a file. The image is saved to your configured media storage
        # using the generated filename.
        response = requests.get(image_url)
        image.image.save(image_name, ContentFile(response.content))
        # The first 'image' refers to model instance
        # The second 'image' refers to the ImageField attribute in your model

        if commit:
            image.save()
        return image

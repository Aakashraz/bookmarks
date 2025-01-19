from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [models.Index(fields=['-created'])]
        ordering = ['-created']
    #     Database indexes improve query performance. Consider creating indexes for fields that you frequently
    # query using filter(), exclude(), or order_by(). ForeignKey fields or fields with unique=True imply
    # the creation of an index.

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    # When an Image object is saved, if the slug field doesn’t have a value, the slugify() function is used
    # to automatically generate a slug from the title field of the image. The object is then saved


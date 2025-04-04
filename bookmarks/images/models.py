from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True, unique=True)
    url = models.URLField(max_length=2000)
    image = models.ImageField(upload_to='images/%Y/%m/%d/')
    # In Django models, when you define an ImageField, it creates an attribute that handles file uploads.
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    users_like = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='images_liked',    # This defines the reverse relationship. From a User object, you can access all the images they've liked using user.images_liked.all().
        blank=True                      # Allow no likes initially
    )
    # Denormalization counts example
    total_likes = models.PositiveIntegerField(default=0)    # to store the total count of users who like each image.

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
            models.Index(fields=['-total_likes']),
        ]
        ordering = ['-created']
    #     Database indexes improve query performance. Consider creating indexes for fields that you frequently
    # query using filter(), exclude(), or order_by(). ForeignKey fields or fields with unique=True imply
    # the creation of an index.

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:   # Generate slug only if it's not already set (for new images).
            # Convert title to URL-friendly format
            # Example: "My Blog Post" -> "my-blog-post"
            base_slug = slugify(self.title)
            counter = 1
            while Image.objects.filter(slug=base_slug).exists():    # check for uniqueness of the slug
                # Append counter for uniqueness
                base_slug = f'{base_slug}-{counter}'
                counter += 1
            self.slug = base_slug

        # call parent class's save() method
        super().save(*args, **kwargs)
    # When an Image object is saved, if the slug field don’t have a value, the slugify() function is used
    # to automatically generate a slug from the title field of the image. The object is then saved

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])

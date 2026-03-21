from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='author_profile')
    display_name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='authors/', blank=True, null=True)
    description = models.TextField(blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    twitch = models.CharField(max_length=100, blank=True)
    youtube = models.CharField(max_length=200, blank=True)
    bluesky = models.CharField(max_length=100, blank=True)
    discord = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.display_name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    main_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    categories = models.ManyToManyField(Category, blank=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-published_at', '-created_at']

    def save(self, *args, **kwargs):
        if self.published and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

from django.contrib import admin
from django import forms
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import BlogPost, Category, Author


class BlogPostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name='default', attrs={'class': 'django_ckeditor_5'}))

    class Meta:
        model = BlogPost
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'user', 'twitter', 'twitch', 'bluesky')
    raw_id_fields = ('user',)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    form = BlogPostAdminForm
    list_display = ('title', 'slug', 'author', 'published', 'published_at', 'created_at')
    readonly_fields = ('published_at', 'created_at')
    list_editable = ('published',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'content')
    list_filter = ('published', 'categories', 'author')
    filter_horizontal = ('categories',)

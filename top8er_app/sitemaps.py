from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import BlogPost


class StaticViewSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ['home', 'blog', 'about', 'contact', 'privacy', 'special-thanks']

    def location(self, item):
        static_paths = {
            'home': '/beta/',
            'blog': '/beta/blog',
            'about': '/beta/about',
            'contact': '/beta/contact',
            'privacy': '/beta/privacy',
            'special-thanks': '/beta/special-thanks',
        }
        return static_paths[item]


class BlogPostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return BlogPost.objects.filter(published=True).order_by('-published_at')

    def lastmod(self, obj):
        return obj.published_at or obj.created_at

    def location(self, obj):
        return f'/beta/blog/{obj.slug}'

from django.urls import path, re_path, include
from django.views.generic.base import TemplateView, RedirectView
from django.contrib.staticfiles.views import serve as serve_static
from django.views.decorators.cache import never_cache
from django.conf import settings

from . import views
from .stuff import games


urlpatterns = [
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/salu2', views.salu2.as_view()),
    path('api/games/', views.api_games.as_view()),
    path('api/game_data/<str:game>/', views.api_game_data.as_view()),
    path('api/templates/', views.api_templates.as_view()),
    path('api/template_data/<str:template>/', views.api_template_data.as_view()),
    path('api/generate/<str:template>/<str:game>/', views.api_generate.as_view()),

    path('test_api/', TemplateView.as_view(template_name="test_api.html")),
    re_path(r'beta/.*', views.react_view),

    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('google6f9c6e66eb07f5ce.html', TemplateView.as_view(template_name="google6f9c6e66eb07f5ce.html"))
]

urlpatterns += [path(slug, views.response_from_game_path(game)) for slug, game in games]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', never_cache(serve_static))
    ]
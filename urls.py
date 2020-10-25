from django.urls import path
from django.views.generic.base import TemplateView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rivals', views.roa, name='rivals'),
    path('skullgirls', views.sg, name='skullgirls'),
    path('RushdownRevolt', views.rr, name='RushdownRevolt'),
    path('melee', views.melee, name='melee'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"))
]

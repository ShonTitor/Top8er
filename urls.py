from django.urls import path
from django.views.generic.base import TemplateView, RedirectView
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rivals', views.roa, name='rivals'),
    path('skullgirls', views.sg, name='skullgirls'),
    path('RushdownRevolt', views.rr, name='RushdownRevolt'),
    path('melee', views.melee, name='melee'),
    path('GuiltyGearACPR', views.ggxx, name='GuiltyGearACPR'),
    path('GuiltyGearXrd', views.ggxrd, name='GuiltyGearXrd'),
    path('GuiltyGearStrive', views.ggst, name='GuiltyGearStrive'),
    path('uni', views.uni, name='uni'),
    path('efz', views.efz, name='efz'),
    path('MeltyBlood', views.mbaacc, name='mbaacc'),
    path('TouhouHisoutensoku', views.soku, name='soku'),
    path('SlapCity', views.slapcity, name='slapcity'),
    path('dfci', views.dfci, name='dfci'),
    path('tla', views.tla, name='tla'),
    path('SpectralVS', views.svs, name='SpectralVS'),
    path('3rdStrike', views.sf3s, name='3rdStrike'),
    path('SuperTurbo', views.sfst, name='SuperTurbo'),
    path('AsuraBuster', views.AsuraBuster, name='AsuraBuster'),
    path('KirbyFighters2', views.kf2, name='KirbyFighters2'),
    path('Project+', views.pplus, name='Project+'),
    path('TFH', views.tfh, name='TFH'),
    path('Wargroove', views.wargroove, name='Wargroove'),
    path('BBTAG', views.bbtag, name='BBTAG'),
    path('WakuWaku7', views.waku, name='Waku Waku 7'),
    path('Windjammers', views.windjammers, name='Windjammers'),
    path('Garou', views.garou, name='Garou Mark of the Wolves'),
    path('SFV', views.sfv, name='Street Fighter V'),
    path('aos2', views.aos2, name='Acceleration of Sugurui 2'),
    path('GBVS', views.gbvs, name='Granblue Fantasy VS'),

    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('google6f9c6e66eb07f5ce.html', TemplateView.as_view(template_name="google6f9c6e66eb07f5ce.html"))
]


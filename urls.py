from django.urls import path, include
from django.views.generic.base import TemplateView, RedirectView
from rest_framework import routers, serializers, viewsets
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
    path('ProjectM', views.pm, name='Project M'),
    path('TFH', views.tfh, name='TFH'),
    path('Wargroove', views.wargroove, name='Wargroove'),
    path('BBTAG', views.bbtag, name='BBTAG'),
    path('WakuWaku7', views.waku, name='Waku Waku 7'),
    path('Windjammers', views.windjammers, name='Windjammers'),
    path('Garou', views.garou, name='Garou Mark of the Wolves'),
    path('SFV', views.sfv, name='Street Fighter V'),
    path('aos2', views.aos2, name='Acceleration of Sugurui 2'),
    path('GBVS', views.gbvs, name='Granblue Fantasy VS'),
    path('amogus', views.amogus, name='Among Us Arena'),
    path('ABK', views.abk, name='Akatsuki Blitzkampf'),
    path('MBTL', views.mbtl, name='Melty Blood Type Lumina'),
    path('dankuga', views.dankuga, name='Dan-Ku-Ga'),
    path('SamuraiShowdownV', views.ssv, name='Samurai Shodown V'),
    path('SamuraiShodownV', views.ssv, name='Samurai Shodown V'),
    path('BBCF', views.bbcf, name='Blazblue Central Fiction'),
    path('NASB', views.nasb, name='Nickelodeon All-Star Brawl'),
    path('VSAV', views.vsav, name='Vampire Savior'),
    path('MvCI', views.mvci, name='Marvel VS Capcom Infinite'),
    path('Tekken7', views.tekken7, name='Tekken 7'),
    path('SSB64', views.ssb64, name='Super Smash Bros 64 Remix'),
    path('Karnov', views.karnov, name='Karnov\'s Revenge'),
    path('SFA3', views.sfa3, name='Alpha 3'),
    path('TheLastBlade2', views.tlb2, name='The Last Blade 2'),
    path('SSBC', views.ssbc, name='Super Smash Bros Crusade'),
    path('BrawlMinus', views.minus, name='Brawl Minus'),
    path('JoyMechFight', views.joymechfight, name='JoyMechFight'),
    path('DBFZ', views.dbfz, name='Dragon Ball FighterZ'),
    path('AvengersGalacticStorm', views.aigs),
    path('MvC2', views.mvc2),
    path('P4AU', views.p4au),
    path('KOFXV', views.kofxv),
    path('TomAndJerry', views.tomandjerry),
    path('KOF2002UM', views.kof2002um),
    path('BreakersRevenge', views.breakersrevenge),
    path('DNFDuel', views.dnf),
    path('Project+TA', views.pplusta),
    path('DoA5', views.doa5),
    path('DoA6', views.doa6),
    path('VHUN', views.vhun),
    path('UltraFightDaKyanta2', views.kyanta2),
    path('Multiversus', views.multiversus),
    path('UMvC3', views.umvc3),
    path('ElemensionalRift', views.elemensional),
    path('SamuraiShodown', views.samsho2019),
    path('Moonatics', views.moonatics),
    path('AntinomyOfCommonFlower', views.touhouantinomy),
    path('VF5', views.vf5),
    #path('SamuraiKirby', views.samuraikirby),


    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/salu2', views.salu2.as_view()),

    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('google6f9c6e66eb07f5ce.html', TemplateView.as_view(template_name="google6f9c6e66eb07f5ce.html"))
]


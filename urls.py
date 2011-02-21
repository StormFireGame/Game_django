from django.conf.urls.defaults import patterns, include, url

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #general
    (r'^$', 'hero.views.main'),
    url(r'^registration/$', 'hero.views.registration', name='registration'),
    
    #hero general
    url(r'^game/$', 'hero.views.hero', name='hero'),
    
    #hero increase
    url(r'^game/hero/increase/(?P<type>abilities)/'
         '(?P<what>swords|axes|knives|clubs|shields)$', 'hero.views.increase', 
         name='hero_increase'),
    url(r'^game/hero/increase/(?P<type>skills)/(?P<what>\d+)$', 
         'hero.views.increase', name='hero_increase'),
    url(r'^game/hero/increase/(?P<type>parameters)/'
         '(?P<what>strength|dexterity|intuition|health)$', 
         'hero.views.increase', name='hero_increase'),
    
    #hero settings
    url(r'^game/settings$', 'hero.views.settings', name='settings'),
    
    #island
    url(r'^game/island/(?P<id>\d+)$', 'island.views.island', name='island'),
    url(r'^game/island/(?P<id>\d+)/move/(?P<coordinate_x>\d+)/'
        '(?P<coordinate_y>\d+)$', 'island.views.move', name='island_move'),
    
    #combat
    #combat forms
    url(r'^game/combat/duel$', 'combat.views.combat_duel', name='combat_duel'),
    url(r'^game/combat/group$', 'combat.views.combat_group', 
        name='combat_group'),
    url(r'^game/combat/chaotic$', 'combat.views.combat_chaotic', 
        name='combat_chaotic'),
    url(r'^game/combat/territorial$', 'combat.views.combat_territorial', 
        name='combat_territorial'),
    url(r'^game/combat/current$', 'combat.views.combat_current', 
        name='combat_current'),
    url(r'^game/combat/past$', 'combat.views.combat_past', name='combat_past'),
    
    #combat actions
    url(r'^game/combat/cancel$', 'combat.views.cancel', name='combat_cancel'),
    url(r'^game/combat/(?P<id>\d+)/accept/(?P<team>0|1)$', 
        'combat.views.accept', name='combat_accept'),
    url(r'^game/combat/refuse$', 'combat.views.refuse', name='combat_refuse'),
    url(r'^game/combat/fight$', 'combat.views.fight', name='combat_fight'),
    
    #combat inside
    url(r'^game/combat$', 'combat.views.combat', name='combat'),
    url(r'^game/combat/quit$', 'combat.views.quit', name='combat_quit'),
    url(r'^game/combat/victory$', 'combat.views.victory', 
        name='combat_victory'),
    
    (r'^admin/', include(admin.site.urls)),
    
    (r'^media/(.*)$', 'django.views.static.serve', 
                                        {'document_root': settings.MEDIA_ROOT})
)

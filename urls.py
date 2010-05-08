from django.conf.urls.defaults import *

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   
    (r'^$', 'hero.views.main'),
    url(r'^registration/$', 'hero.views.registration', name='registration'),
    
    url(r'^game/$', 'hero.views.hero', name='hero'),
    
    url(r'^game/hero/increase/(?P<type>abilities)/'
         '(?P<what>swords|axes|knives|clubs|shields)$', 'hero.views.increase', 
         name='hero_increase'),
    url(r'^game/hero/increase/(?P<type>skills)/(?P<what>\d+)$', 
         'hero.views.increase', name='hero_increase'),
    url(r'^game/hero/increase/(?P<type>parameters)/'
         '(?P<what>strength|dexterity|intuition|health)$', 
         'hero.views.increase', name='hero_increase'),
    
    url(r'^game/settings$', 'hero.views.settings', name='settings'),
    
    url(r'^game/island/(?P<id>\d+)$', 'island.views.island', name='island'),
    url(r'^game/island/(?P<id>\d+)/move/(?P<coordinate_x>\d+)/'
        '(?P<coordinate_y>\d+)$', 'island.views.move', name='island_move'),
        
    url(r'^game/combat/(?P<type>0|1|2|3|4|5)$', 'combat.views.combat', 
        name='combat'),
    url(r'^game/combat/cancel$', 'combat.views.cancel', name='combat_cancel'),
    url(r'^game/combat/(?P<id>\d+)/accept/(?P<team>0|1)$', 
        'combat.views.accept', name='combat_accept'),
    url(r'^game/combat/refuse$', 'combat.views.refuse', name='combat_refuse'),
    
    (r'^admin/', include(admin.site.urls)),
    
    (r'^media/(.*)$', 'django.views.static.serve', 
                                        {'document_root': settings.MEDIA_ROOT})
)

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
       
    (r'^admin/', include(admin.site.urls)),
    
    (r'^media/(.*)$', 'django.views.static.serve', 
                                        {'document_root': settings.MEDIA_ROOT})
)

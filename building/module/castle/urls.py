from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('building.module.castle.views',
                       url(r'^(?P<slug>[-\w]+)$', 'index', name='castle'))
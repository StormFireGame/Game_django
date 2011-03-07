from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('building.module.street.views',
                       url(r'^(?P<slug>[-\w]+)$', 'index', name='street'))
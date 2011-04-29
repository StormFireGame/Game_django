from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('building.module.buyingup.views',
                       url(r'^(?P<slug>[-\w]+)$', 'index', name='buyingup'),
                       url(r'^(?P<slug>[-\w]+)/view/'
                           '(?P<type>sword|axe|knive|clubs|shield|helmet|'
                           'kolchuga|armor|belt|pants|treetop|glove|boot|'
                           'ring|amulet)$', 'view', name='buyingup_view'),
                       url(r'^(?P<slug>[-\w]+)/sell/(?P<herothing_id>\d+)$',
                           'sell', name='buyingup_sell'), 
                      )
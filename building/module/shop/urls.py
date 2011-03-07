from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('building.module.shop.views',
                       url(r'^(?P<slug>[-\w]+)$', 'index', name='shop'),
                       url(r'^(?P<slug>[-\w]+)/view/'
                           '(?P<type>sword|axe|knive|clubs|shield|helmet|'
                           'kolchuga|armor|belt|pants|treetop|glove|boot|'
                           'ring|amulet)$', 'view', name='shop_view'),
                       url(r'^(?P<slug>[-\w]+)/buy/(?P<id>\d+)$', 
                           'buy', name='shop_buy'), 
                      )
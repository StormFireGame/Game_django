from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('building.module.commission.views',
                       url(r'^(?P<slug>[-\w]+)$', 'index', name='commission'),
                       url(r'^(?P<slug>[-\w]+)/view/'
                           '(?P<type>sword|axe|knive|clubs|shield|helmet|'
                           'kolchuga|armor|belt|pants|treetop|glove|boot|'
                           'ring|amulet)$', 'view', name='commission_view'),
                       
                       url(r'^(?P<slug>[-\w]+)/put$', 'put', 
                           name='commission_put'),
                       url(r'^(?P<slug>[-\w]+)/putselect/(?P<id>\d+)$', 
                           'put_select', name='commission_put_select'),
                           
                       url(r'^(?P<slug>[-\w]+)/buy/(?P<id>\d+)$', 'buy', 
                           name='commission_buy'),
                           
                       url(r'^(?P<slug>[-\w]+)/take$', 'take', 
                           name='commission_take'),
                       url(r'^(?P<slug>[-\w]+)/takeselect/(?P<id>\d+)$', 
                           'take_select', name='commission_take_select'),
                      )
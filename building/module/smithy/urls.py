from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('building.module.smithy.views',
                       url(r'^(?P<slug>[-\w]+)$', 'index', name='smithy'),
                       
                       url(r'^(?P<slug>[-\w]+)/repair$', 'repair', 
                           name='smithy_repair'), 
                       url(r'^(?P<slug>[-\w]+)/repairone/(?P<id>\d+)$', 
                           'repair_one', name='smithy_repair_one'), 
                       url(r'^(?P<slug>[-\w]+)/repairfull/(?P<id>\d+)$', 
                           'repair_full', name='smithy_repair_full'),
                       
                       url(r'^(?P<slug>[-\w]+)/modify$', 'modify', 
                           name='smithy_modify'),
                       url(r'^(?P<slug>[-\w]+)/modifyselect/'
                            '(?P<id_herothing>\d+)/(?P<id_smithyfeature>\d+)$', 
                           'modify_select', name='smithy_modify_select'),
                      )
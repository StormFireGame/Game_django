from django.conf.urls.defaults import patterns, include, url

from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Main
    url(r'^$', 'main.views.main', name='main'),
    url(r'^registration$', 'main.views.registration', name='registration'),

    # Hero
    # Hero general
    url(r'^game$', 'hero.views.hero', name='hero'),
    
    # Hero increase
    url(r'^game/hero/increase/(?P<type>abilities)/'
         '(?P<what>swords|axes|knives|clubs|shields)$', 'hero.views.increase', 
         name='hero_increase'),
    url(r'^game/hero/increase/(?P<type>skills)/(?P<what>\d+)$', 
         'hero.views.increase', name='hero_increase'),
    url(r'^game/hero/increase/(?P<type>parameters)/'
         '(?P<what>strength|dexterity|intuition|health)$', 
         'hero.views.increase', name='hero_increase'),
    
    # Hero inventory
    url(r'^game/inventory$', 'hero.views.inventory', name='hero_inventory'),
    url(r'^game/inventory/throw/(?P<herothing_id>\d+)$', 'hero.views.throw',
        name='hero_inventory_throw'),
    url(r'^game/inventory/dress/(?P<herothing_id>\d+)$', 'hero.views.dress',
        name='hero_inventory_dress'),
    url(r'^game/inventory/undress/(?P<herothing_id>\d+)$',
        'hero.views.undress', name='hero_inventory_undress'),
    url(r'^game/inventory/undressall$', 'hero.views.undressall', 
        name='hero_inventory_undressall'),
    
    # Hero preferences
    url(r'^game/preferences$', 'hero.views.preferences',
        name='hero_preferences'),
    # End hero

    # Island
    url(r'^game/island$', 'island.views.island', name='island'),
    url(r'^game/island/move/(?P<coordinate_x>\d+)/'
        '(?P<coordinate_y>\d+)$', 'island.views.move', name='island_move'),
    url(r'^game/botattack/(?P<bot_id>\d+)', 'island.views.bot_attack', 
        name='island_bot_attack'),
    
    # Combat
    # Combat forms
    url(r'^game/combat/duel$', 'combat.views.duel', name='combat_duel'),
    url(r'^game/combat/group$', 'combat.views.group', name='combat_group'),
    url(r'^game/combat/chaotic$', 'combat.views.chaotic',
        name='combat_chaotic'),
    url(r'^game/combat/territorial$', 'combat.views.territorial',
        name='combat_territorial'),
    url(r'^game/combat/current$', 'combat.views.current',
        name='combat_current'),
    url(r'^game/combat/past$', 'combat.views.past', name='combat_past'),
    
    # Combat actions
    url(r'^game/combat/cancel$', 'combat.views.cancel', name='combat_cancel'),
    url(r'^game/combat/(?P<combat_id>\d+)/accept/(?P<team>0|1)$',
        'combat.views.accept', name='combat_accept'),
    url(r'^game/combat/refuse$', 'combat.views.refuse', name='combat_refuse'),
    url(r'^game/combat/fight$', 'combat.views.fight', name='combat_fight'),
    url(r'^game/combat/(?P<combat_id>\d+)/enter/(?P<team>0|1)$', 'combat.views.enter',
        name='combat_enter'),
    
    # Combat inside
    url(r'^game/combat$', 'combat.views.combat', name='combat'),
    url(r'^game/combat/quit$', 'combat.views.quit', name='combat_quit'),
    url(r'^game/combat/victory$', 'combat.views.victory', 
        name='combat_victory'),
    
    # Building modules
    (r'^game/building/castle/', include('building.module.castle.urls')),
    (r'^game/building/street/', include('building.module.street.urls')),
    (r'^game/building/shop/', include('building.module.shop.urls')),
    (r'^game/building/buyingup/', include('building.module.buyingup.urls')),
    (r'^game/building/commission/', 
     include('building.module.commission.urls')),
    (r'^game/building/smithy/', include('building.module.smithy.urls')),
    
    (r'^admin/', include(admin.site.urls)),
    
    (r'^media/(.*)$', 'django.views.static.serve', 
     {'document_root': settings.MEDIA_ROOT}),
    
    # (r'^sentry/', include('sentry.urls')),
)

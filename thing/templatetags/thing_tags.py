from django import template
from django.db.models import Q

from thing.models import Thing 

register = template.Library()

def do_thing_requirement(parser, token):
    try:
        tag_name, need_attr, hero_attr = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly two'
                                    ' arguments' % (token.contents.split()[0]))
    return ThingRequirementNode(need_attr, hero_attr)

class ThingRequirementNode(template.Node):
    def __init__(self, need_attr, hero_attr):
        self.need_attr = template.Variable(need_attr)
        self.hero_attr = template.Variable(hero_attr)
        
    def render(self, context):
        need_attr = self.need_attr.resolve(context)
        hero_attr = self.hero_attr.resolve(context)
        
        if need_attr > int(hero_attr):
            return '<span class="red">' + str(need_attr) + '</span>'
        return need_attr
    
register.tag('get_thing_requirement', do_thing_requirement)

def do_is_can_dress(parser, token):
    try:
        tag_name, hero, thing, sa, context_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly fourth'
                                    ' arguments' % (token.contents.split()[0]))
    if sa != 'as':
        raise template.TemplateSyntaxError('Third argument must be as')
    return GetIsCanDressNode(hero, thing, context_var)

class GetIsCanDressNode(template.Node):
    def __init__(self, hero, thing, context_var):
        self.hero = template.Variable(hero)
        self.thing = template.Variable(thing)
        self.context_var = context_var

    def render(self, context):
        hero = self.hero.resolve(context)
        thing = self.thing.resolve(context)
        
        if hero.level >= thing.level_need and \
           int(hero.feature.strength) >= thing.strength_need and \
           int(hero.feature.dexterity) >= thing.dexterity_need and \
           int(hero.feature.intuition) >= thing.intuition_need and \
           int(hero.feature.health) >= thing.health_need and \
           int(hero.feature.swords) >= thing.swords_need and \
           int(hero.feature.axes) >= thing.axes_need and \
           int(hero.feature.knives) >= thing.knives_need and \
           int(hero.feature.clubs) >= thing.clubs_need and \
           int(hero.feature.shields) >= thing.shields_need:
            context[self.context_var] = True
        else:
            context[self.context_var] = False
        
        return ''
        
register.tag('get_is_can_dress', do_is_can_dress)

def do_hero_dressed_things(parser, token):
    try:
        tag_name, hero, sa, context_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly three'
                                    ' arguments' % (token.contents.split()[0]))
    if sa != 'as':
        raise template.TemplateSyntaxError('Third argument must be as')
    return GetHeroDressedThingsNode(hero, context_var)

class GetHeroDressedThingsNode(template.Node):
    def __init__(self, hero, context_var):
        self.hero = template.Variable(hero)
        self.context_var = context_var

    def render(self, context):
        hero = self.hero.resolve(context)
        
        context[self.context_var] = hero.herothing_set.filter(dressed=True)
        
        return ''
        
register.tag('get_hero_dressed_things', do_hero_dressed_things)

def do_class_position(parser, token):
    try:
        tag_name, herothing, herothings = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly two'
                                    ' arguments' % (token.contents.split()[0]))
    return GetClassPosition(herothing, herothings)

class GetClassPosition(template.Node):
    def __init__(self, herothing, herothings):
        self.herothing = template.Variable(herothing)
        self.herothings = template.Variable(herothings)

    def render(self, context):
        herothing = self.herothing.resolve(context)
        herothings = self.herothings.resolve(context)
        
        type = herothing.thing.type
        
        if type == Thing.TYPE_HELMET:
            return 'helmet'
        elif type == Thing.TYPE_KOLCHUGA:
            return 'kolchuga'
        elif type == Thing.TYPE_ARMOR:
            return 'armor'
        elif type == Thing.TYPE_BELT:
            return 'belt'
        elif type == Thing.TYPE_PANTS:
            return 'pants'
        elif type == Thing.TYPE_TREETOP:
            return 'treetop'
        elif type == Thing.TYPE_GLOVE:
            return 'glove'
        elif type == Thing.TYPE_BOOT:
            return 'boot'
        elif type == Thing.TYPE_AMULET:
            return 'amulet'
        elif type == Thing.TYPE_RING:
            herothings = herothings.filter(thing__type=type)
            num_ring = 0
            for ring in herothings:
                if ring.id == herothing.id:
                    break
                num_ring += 1
            return 'ring' + str(num_ring)
        elif type == Thing.TYPE_SWORD or type == Thing.TYPE_AXE or \
             type == Thing.TYPE_KNIVE or type == Thing.TYPE_CLUBS or \
             type == Thing.TYPE_SHIELD:
            herothings = herothings.filter(Q(thing__type=Thing.TYPE_SWORD) | 
                                           Q(thing__type=Thing.TYPE_AXE) |
                                           Q(thing__type=Thing.TYPE_KNIVE) |
                                           Q(thing__type=Thing.TYPE_CLUBS) |
                                           Q(thing__type=Thing.TYPE_SHIELD))
            
            has_shield = False
            i = 0
            for arms in herothings:
                if arms.thing.type == Thing.TYPE_SHIELD:
                    has_shield = True
                    break
                if arms.id == herothing.id:
                    num_arms = i
                i += 1
            
            if has_shield == True:
                if type == Thing.TYPE_SHIELD:
                    num_arms = 1
                else:
                    num_arms = 0
            
            return 'arms' + str(num_arms)
            
        return ''
    
register.tag('get_class_position', do_class_position)
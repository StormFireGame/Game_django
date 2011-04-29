from django import template

from django.core.urlresolvers import reverse

register = template.Library()

def do_hero_feature(parser, token):
    try:
        tag_name, parametr, feature_parametr = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly two'
                                    ' arguments' % (token.contents.split()[0]))
    return HeroFeatureNode(parametr, feature_parametr)

class HeroFeatureNode(template.Node):
    def __init__(self, parametr, feature_parametr):
        self.parametr = template.Variable(parametr)
        self.feature_parametr = template.Variable(feature_parametr)

    def render(self, context):
        parametr = int(self.parametr.resolve(context))
        feature_parametr = int(self.feature_parametr.resolve(context))
        if feature_parametr != parametr:
            symbol = ''
            if feature_parametr > parametr:
                symbol = '+'
            return '[%s%s]' % (symbol, (feature_parametr - parametr))
        else:
            return ''
        
register.tag('get_hero_feature', do_hero_feature)

def do_hero_skill(parser, token):
    try:
        tag_name, hero, heroskill = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly two'
                                    ' arguments' % (token.contents.split()[0]))
    return HeroSkillNode(hero, heroskill)

class HeroSkillNode(template.Node):
    def __init__(self, hero, heroskill):
        self.hero = template.Variable(hero)
        self.heroskill = template.Variable(heroskill)

    def render(self, context):
        hero = self.hero.resolve(context)
        heroskill = self.heroskill.resolve(context)
        
        try:
            return hero.heroheroskill_set.get(skill=heroskill).level
        except:
            return '0'
        
register.tag('get_hero_skill', do_hero_skill)

def do_back_url(parser, token):
    try:
        tag_name, location, request = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly two'
                                    ' arguments' % (token.contents.split()[0]))
    return BackUrlNode(location, request)

class BackUrlNode(template.Node):
    def __init__(self, location, request):
        self.location = template.Variable(location)
        self.request = template.Variable(request)

    def render(self, context):
        location = self.location.resolve(context)
        request = self.request.resolve(context)
        
        in_building = 'building' in request.path.split('/')
        locations = location.split('&')
        index = len(locations) - 1
        if in_building:
            index -= 1
        
        if index == 0:
            return reverse('island')
        else:
            plugin, slug = locations[index].split(':')
            return reverse(plugin, args=[slug])
            
register.tag('get_back_url', do_back_url)
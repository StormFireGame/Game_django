from django import template

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
        tag_name, heroskills, skill = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly two'
                                    ' arguments' % (token.contents.split()[0]))
    return HeroSkillNode(heroskills, skill)

class HeroSkillNode(template.Node):
    def __init__(self, heroskills, skill):
        self.hero = template.Variable(heroskills)
        self.skill = template.Variable(skill)

    def render(self, context):
        hero = self.hero.resolve(context)
        heroskill = self.skill.resolve(context)
        
        try:
            return hero.heroheroskill_set.get(skill=heroskill).level
        except:
            return '0'
        
register.tag('get_hero_skill', do_hero_skill)
from django import template

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
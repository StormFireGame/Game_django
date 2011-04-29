from django import template

from django.core.urlresolvers import reverse

register = template.Library()

def do_building_url(parser, token):
    try:
        tag_name, building = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly one'
                                    ' arguments' % (token.contents.split()[0]))
    return BuildingUrlNode(building)

class BuildingUrlNode(template.Node):
    def __init__(self, building):
        self.building = template.Variable(building)
        
    def render(self, context):
        building = self.building.resolve(context)
        return reverse(building.module, args=[building.slug])
        
register.tag('get_building_url', do_building_url)

def do_building_image(parser, token):
    try:
        tag_name, building_image, defaut_child_building = \
                                                        token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly two'
                                    ' arguments' % (token.contents.split()[0]))
    return BuildingImageNode(building_image, defaut_child_building)

class BuildingImageNode(template.Node):
    def __init__(self, building_image, defaut_child_building):
        self.building_image = template.Variable(building_image)
        self.defaut_child_building = template.Variable(defaut_child_building)
        
    def render(self, context):
        building_image = self.building_image.resolve(context)
        defaut_child_building = self.defaut_child_building.resolve(context)
        
        if defaut_child_building:
            return defaut_child_building.image
        return building_image
        
register.tag('get_building_image', do_building_image)
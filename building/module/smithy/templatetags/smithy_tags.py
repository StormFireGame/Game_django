from django import template

register = template.Library()

def do_get_price_for_repair(parser, token):
    try:
        tag_name, herothing, percent_repair_money, count, sa, context_var = \
                                                        token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly fifth'
                                    ' arguments' % (token.contents.split()[0]))
    if sa != 'as':
        raise template.TemplateSyntaxError('Third argument must be as')
    return GetPriceForRepair(herothing, percent_repair_money, count, 
                             context_var)

class GetPriceForRepair(template.Node):
    def __init__(self, herothing, percent_repair_money, count, context_var):
        self.herothing = template.Variable(herothing)
        self.percent_repair_money = template.Variable(percent_repair_money)
        self.count = count
        self.context_var = context_var
    
    def render(self, context):
        herothing = self.herothing.resolve(context)
        percent_repair_money = self.percent_repair_money.resolve(context)
        count = int(self.count)
        
        if not count:
            count = herothing.stability_left - herothing.stability_all
        
        context[self.context_var] = float(count * 
                                                   (herothing.thing.price * 
                                                (percent_repair_money / 100)))
        return ''
            
register.tag('get_price_for_repair', do_get_price_for_repair)
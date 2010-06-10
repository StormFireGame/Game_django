from django import template

register = template.Library()

def do_get_team(parser, token):
    try:
        tag_name, combatheroes, team, sa, context_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly fourth'
                                    ' arguments' % (token.contents.split()[0]))
    if sa != 'as':
        raise template.TemplateSyntaxError('Third argument must be as')
    return GetTeamNode(combatheroes, team, context_var)

class GetTeamNode(template.Node):
    def __init__(self, combatheroes, team, context_var):
        self.combatheroes = template.Variable(combatheroes)
        self.team = template.Variable(team)
        self.context_var = context_var

    def render(self, context):
        combatheroes = self.combatheroes.resolve(context)
        team = int(self.team.resolve(context))
        
        context[self.context_var] = combatheroes.filter(team=team)
        return ''
            
register.tag('get_team', do_get_team)

def do_get_team_accept(parser, token):
    try:
        tag_name, combat, hero, team, sa, context_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly fifth'
                                    ' arguments' % (token.contents.split()[0]))
    if sa != 'as':
        raise template.TemplateSyntaxError('Fourth argument must be as')
    return GetTeamAcceptNode(combat, hero, team, context_var)

class GetTeamAcceptNode(template.Node):
    def __init__(self, combat, hero, team, context_var):
        self.combat = template.Variable(combat)
        self.hero = template.Variable(hero)
        self.team = template.Variable(team)
        self.context_var = context_var

    def render(self, context):
        combat = self.combat.resolve(context)
        hero = self.hero.resolve(context)
        team = int(self.team.resolve(context))
        
        if team == 0:
            team_count = combat.one_team_count
            team_lvl_min = combat.one_team_lvl_min
            team_lvl_max = combat.one_team_lvl_max
        else:
            team_count = combat.two_team_count
            team_lvl_min = combat.two_team_lvl_min
            team_lvl_max = combat.two_team_lvl_max
        
        team_count_now = combat.combathero_set.filter(team=team).count()
        
        if hero.level >= team_lvl_min and hero.level <= team_lvl_max and \
            team_count_now < team_count:    
            context[self.context_var] = True
        else:
            context[self.context_var] = False
        return ''
            
register.tag('get_team_accept', do_get_team_accept)

def get_hero_strike(parser, token):
    try:
        tag_name, form, strike, where = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly three'
                                    ' arguments' % (token.contents.split()[0]))
    return HeroStrikeNode(form, strike, where)

class HeroStrikeNode(template.Node):
    def __init__(self, form, strike, where):
        self.form = template.Variable(form)
        self.strike = template.Variable(strike)
        self.where = template.Variable(where)
        
    def render(self, context):
        form = self.form.resolve(context)
        strike = str(self.strike.resolve(context))
        where = self.where.resolve(context)
        
        try:
            form.clean
            if form.data['strike'+strike] == where:
                return 'checked="checked"'
        except:
            pass 
        return ''
        
register.tag('get_hero_strike', get_hero_strike)

def do_get_team_in_combat(parser, token):
    try:
        tag_name, combatheroes, team, sa, context_var = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly fourth'
                                    ' arguments' % (token.contents.split()[0]))
    if sa != 'as':
        raise template.TemplateSyntaxError('Third argument must be as')
    return GetTeamInCombatNode(combatheroes, team, context_var)

class GetTeamInCombatNode(template.Node):
    def __init__(self, combatheroes, team, context_var):
        self.combatheroes = template.Variable(combatheroes)
        self.team = template.Variable(team)
        self.context_var = context_var

    def render(self, context):
        combatheroes = self.combatheroes.resolve(context)
        team = int(self.team.resolve(context))
        
        context[self.context_var] = combatheroes.filter(team=team, 
                                                        is_dead=False)
        return ''
            
register.tag('get_team_in_combat', do_get_team_in_combat)
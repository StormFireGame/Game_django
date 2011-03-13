import re

from combat.models import Combat

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

def do_get_friendly_log(parser, token):
    try:
        tag_name, combatlog = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError('%s tag takes exactly one'
                                    ' arguments' % (token.contents.split()[0]))
    
    return GetFriendlyLogNode(combatlog)

class GetFriendlyLogNode(template.Node):
    def __init__(self, combatlog):
        self.combatlog = template.Variable(combatlog)
        
    def render(self, context):
        combatlog = self.combatlog.resolve(context)
        
        log = combatlog.time.strftime('%H:%M ')

        if combatlog.is_start:
            # Fight between ButuzGOL [0] vs Fog [0] start
            log += 'Fight between ' + \
    re.search('\[heroes_one](.*)\[\/heroes_one]', combatlog.text).group(1) + \
                                                                    ' vs ' + \
    re.search('\[heroes_two](.*)\[\/heroes_two]', combatlog.text).group(1) + \
                                                                    ' start'
        elif combatlog.is_dead:
            # ButuzGOL[0] is dead
            log += re.search('\[hero](.*)\[\/hero]', 
                             combatlog.text).group(1) + 'is dead'
        elif combatlog.is_finish:
            # Fight between ButuzGOL [0] vs Fog [0] ended in a draw
            # Victory for ButuzGOL [0]
            if re.search('\[heroes_two](.*)\[\/heroes_two]', combatlog.text):
                log += 'Fight between ' + \
    re.search('\[heroes_one](.*)\[\/heroes_one]', combatlog.text).group(1) + \
                                                                    ' vs ' + \
    re.search('\[heroes_two](.*)\[\/heroes_two]', combatlog.text).group(1) + \
                                                            ' ended in a draw'
            else:
                log += 'Victory for ' + \
        re.search('\[heroes_one](.*)\[\/heroes_one]', combatlog.text).group(1)                                                           
            
        else:
            # ButuzGOL[0] struck Fog[0] on -5 (head) (head, breast)
            ## ButuzGOL[0] break armor struck Fog[0] on -10
            ## ButuzGOL[0] struck critical hit Fog[0] on -10
            ## ButuzGOL[0] break armor struck critical hit Fog[0] on -10
            ## ButuzGOL[0] struck critical but blocked Fog[0] on -10
            # ButuzGOL[0] break block critical hit struck Fog[0] on -10
            # ButuzGOL[0] break block break armor critical hit struck Fog[0] 
            # on -10
            # ButuzGOL[0] make strike but dodged Fog[0]
            # ButuzGOL[0] make strike but blocked Fog[0]           
            
            hero_bumps = combatlog.text.split(':')
            for hero_bump in hero_bumps:
                bumps = hero_bump.split('&')
                for bump in bumps:
                    hero_one = \
                    re.search('\[hero_one](.*)\[\/hero_one]', bump).group(1)
                    hero_two = \
                    re.search('\[hero_two](.*)\[\/hero_two]', bump).group(1)
                    strikes = re.search('\[strikes](.*)\[\/strikes]', bump). \
                                                            group(1).split('|')
                    blocks = re.search('\[blocks](.*)\[\/blocks]', bump). \
                                                            group(1).split('|')
                    strike_w = []
                    for strike in strikes:
                        strike_p = [ int(i) for i in strike.split('_') ]
                        if strike_p[2] and strike_p[3] == False and \
                           strike_p[5] == False:
                            log += hero_one + ' make strike but blocked ' + \
                                                                    hero_two
                        elif strike_p[4]:
                            log += hero_one + ' make strike but dodged ' + \
                                                                    hero_two 
                        elif strike_p[3] and strike_p[2] and strike_p[6] and \
                             strike_p[5]:
                            log += hero_one + ' break block break armor ' + \
                                   'critical hit struck ' + hero_two + \
                                   ' on -' + str(strike_p[1])
                        elif strike_p[3] and strike_p[2] and strike_p[5]:
                            log += hero_one + \
                                   ' break block critical hit struck ' + \
                                   hero_two + ' on -' + str(strike_p[1])
                        elif strike_p[5] and strike_p[2]:
                            log += hero_one + \
                                   ' struck critical but blocked ' + \
                                   hero_two + ' on -' + str(strike_p[1])
                        elif strike_p[6] and strike_p[5]:
                            log += hero_one + \
                                   ' break armor struck critical hit ' + \
                                   hero_two + ' on -' + str(strike_p[1])
                        elif strike_p[5]:
                            log += hero_one + ' struck critical hit ' + \
                                   hero_two + ' on -' + str(strike_p[1])
                        elif strike_p[6]:
                            log += hero_one + ' break armor struck ' + \
                                   hero_two + ' on -' + str(strike_p[1])
                        else:
                            log += hero_one + ' struck ' + hero_two + \
                                   ' on -' + str(strike_p[1])
                        strike_w.append(strike_p[0])
                        
                    
                    strike_w = [ Combat.STRIKES[int(i)][1] for i in strike_w ]
                    blocks_w = [ Combat.BLOCKS[int(i)][1] for i in blocks ]
                    log += ' (' + ', '.join(strike_w) + ') (' + \
                           ', '.join(blocks_w) + ') '
        return log
            
register.tag('get_friendly_log', do_get_friendly_log)
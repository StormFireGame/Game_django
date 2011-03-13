from combat.models import Combat, CombatLog
from tableexperience.models import TableExperience

import time
import random
import datetime

def get_location(location):
    return location.split(':')[0]

def in_combat(hero, is_active=Combat.IS_ACTIVE_WAIT):
    try:
        combat = Combat.objects.filter(combathero__hero=hero, 
                                       is_active=is_active, 
                                       combathero__is_quit=False).get()
        return combat
    except Combat.DoesNotExist:
        return False

def is_cancel(hero):
    try:
        combat = Combat.objects.filter(combathero__hero=hero, 
                                       is_active=Combat.IS_ACTIVE_WAIT).get()
        if combat.combathero_set.count() == 1:
            return True
        else:
            return False
    except Combat.DoesNotExist:
        return False

def is_combat(hero):
    return in_combat(hero, Combat.IS_ACTIVE_FIGHT) != False

# For duel
def is_fight(hero):
    try:
        combat = \
            Combat.objects.filter(combathero__hero=hero, 
                                  combathero__team=Combat.TEAM_FIRST, 
                                  type=Combat.TYPE_DUEL, 
                                  is_active=Combat.IS_ACTIVE_WAIT).get()
        return combat.combathero_set.count() == 2
    except Combat.DoesNotExist:
        return False

def is_refuse(hero):
    try:
        combat = Combat.objects.filter(combathero__hero=hero, 
                                       type=Combat.TYPE_DUEL, 
                                       is_active=Combat.IS_ACTIVE_WAIT).get()
        if combat.combathero_set.count() == 2:
            return combat
    except Combat.DoesNotExist:
        pass
    return False

def update_combats(type):
    combats = Combat.objects.filter(type=type, is_active=Combat.IS_ACTIVE_WAIT)
    
    for combat in combats:
        one_team_count = combat.combathero_set. \
                                        filter(team=Combat.TEAM_FIRST).count()
        two_team_count = combat.combathero_set. \
                                        filter(team=Combat.TEAM_SECOND).count()
        
        if (one_team_count == combat.one_team_count and
           two_team_count == combat.two_team_count and \
           type == Combat.TEAM_SECOND) or \
           (one_team_count == combat.one_team_count and \
            type == Combat.TYPE_CHAOTIC):
            _start_combat(combat, type)
            continue
        
        time_start = int(time.mktime(combat.start_date_time.timetuple()))
        if (int(time.time()) - time_start) >= combat.time_wait:
            if (one_team_count > 0 and two_team_count > 0 and 
                type == Combat.TYPE_GROUP) or \
                (one_team_count > 0 and type == Combat.TYPE_CHAOTIC):
                _start_combat(combat, type)
            else:
                combat.delete()
        else:
            combat.time_wait_left = combat.time_wait - (int(time.time()) -
                                                                    time_start)   
            combat.save()

def _start_combat(combat, type):
    if type == Combat.TYPE_CHAOTIC:
        
        count = combat.combathero_set.count()
        count_to_replace = count / 2
        if count % 2:
            if (random.randint(0, 1)):
                count_to_replace = (count + 1) / 2
            
        to_replace = []
        for i in range(count_to_replace):
            while True:
                rand = random.randint(0, (count-1))
                if rand not in to_replace:
                    break
            to_replace.append(rand)
            
        combatheroes = combat.combathero_set.all()
        for i in to_replace:
            combathero = combat.combathero_set.get(pk=combatheroes[i].id)
            combathero.team = Combat.TEAM_SECOND
            combathero.save()
            
    combat.is_active = Combat.IS_ACTIVE_FIGHT
    combat.save()
# End

#Combat inside
def is_dead(combat, hero):
    return combat.combathero_set.filter(hero=hero, is_dead=True).exists()

def is_draw(combat):
    return combat.combathero_set.all().count() == \
                            combat.combathero_set.filter(is_dead=True).count()
    
def is_win(combat, team, is_draw):
    return not combat.combathero_set.filter(is_dead=False). \
                                exclude(team=team).exists() and not is_draw

def is_lose(combat, team, is_draw):
    return not combat.combathero_set.filter(is_dead=False, team=team). \
                                                    exists() and not is_draw
                                                    
def get_enemies(combat, hero, team):
    if team == Combat.TEAM_FIRST:
        enemies = [ i.hero for i in combat.combathero_set.
                                    filter(is_dead=False).exclude(team=team) 
                    if not combat.combatlog_set.filter(hero_one=hero, 
                                                       hero_two=i.hero, 
                                                       is_past=False, 
                                                       hero_two_wstrike=None) ]  
    else:
        enemies = [ i.hero for i in combat.combathero_set. \
                                    filter(is_dead=False).exclude(team=team) 
                    if not combat.combatlog_set.filter(hero_two=hero, 
                                                       hero_one=i.hero, 
                                                       is_past=False, 
                                                       hero_one_wstrike=None) ]
        
    return enemies

def get_enemy(enemies, cur_enemy_id_fn):
    index = 0
    if cur_enemy_id_fn:
        i = 0
        for enemy in enemies:
            i += 1
            if enemy.id == cur_enemy_id_fn:
                index = i
                break
        if index == len(enemies):
            index = 0
            
    return enemies[index] if enemies else None

def get_combat_log(combat, hero, hero_two, team):
    try:
        if team == Combat.TEAM_FIRST:
            return combat.combatlog_set.filter(hero_one=hero, 
                                               hero_two=hero_two,
                                               is_past=False).get()
        else:
            return combat.combatlog_set.filter(hero_two=hero,
                                               hero_one=hero_two,
                                               is_past=False).get()
    except CombatLog.DoesNotExist:
        return None
                                                        
def write_log_messages(combat, is_start=False, is_finish=False, win_team=None, 
                       is_dead=False, hero=None):
    if is_start:
        if combat.combatlog_set.filter(is_start=True).exists():
            return
        
        heroes_one = [ str(i.hero) for i in combat.combathero_set. \
                                            filter(team=Combat.TEAM_FIRST) ]
        heroes_two = [ str(i.hero) for i in combat.combathero_set. \
                                            filter(team=Combat.TEAM_SECOND) ]
        
        combat.combatlog_set.create(is_start=True, \
                text='[heroes_one]' + ','.join(heroes_one) + '[/heroes_one]'
                     + '[heroes_two]' + ','.join(heroes_two) + '[/heroes_two]')
    
    if is_finish:
        if combat.combatlog_set.filter(is_finish=True).exists():
            return
    
        if win_team == None:
            heroes_one = [ str(i.hero) for i in combat.combathero_set. \
                                            filter(team=Combat.TEAM_FIRST) ]
            heroes_two = [ str(i.hero) for i in combat.combathero_set. \
                                            filter(team=Combat.TEAM_SECOND) ]
            combat.combatlog_set.create(is_finish=True, 
                text='[heroes_one]' + ','.join(heroes_one) + '[/heroes_one]' + 
                     '[heroes_two]' + ','.join(heroes_two) + '[/heroes_two]')
        else:
            heroes = [ str(i.hero) for i in combat.combathero_set.
                                                        filter(team=win_team) ]
            combat.combatlog_set.create(is_finish=True,
                    text='[heroes_one]' + ','.join(heroes) + '[/heroes_one]')
    
    if is_dead:
        combat.combatlog_set.create(is_dead=True, hero_one=hero,
                                    text='[hero]' + str(hero) + '[/hero]')

##
def write_log_strikes(combat, combatlog, team, hero, hero_two, 
                      strikes, blocks):
    if combatlog is None:
        strikes_s = '|'.join(strikes)
        blocks_s = '|'.join(blocks)
     
        if team == Combat.TEAM_FIRST:
            combatlog = combat.combatlog_set.create(hero_one=hero,
                                                    hero_two=hero_two,
                                                    hero_one_wstrike=strikes_s,
                                                    hero_one_wblock=blocks_s)
        else:
            combatlog = combat.combatlog_set.create(hero_one=hero_two,
                                                    hero_two=hero,
                                                    hero_two_wstrike=strikes_s,
                                                    hero_two_wblock=blocks_s)
    else:
        from hero.heromanipulation import set_hp
        if team == Combat.TEAM_FIRST:
            strikes_two = combatlog.hero_two_wstrike.split('|')
            blocks_two = combatlog.hero_two_wblock.split('|')
        else:
            strikes_two = combatlog.hero_one_wstrike.split('|')
            blocks_two = combatlog.hero_one_wblock.split('|')
        
        thero = hero
        thero_two = hero_two
            
        accuracy_p = 500
        devastate_p = 500
        block_break_p = 1000
        armor_break_p = 1000
        damage_p = 10
        
        dead_heroes = []
        combatlog.text = ''
        for j in range(2):
            if j == 1:
                strikes = strikes_two
                blocks_two = blocks
                team = int(not team)
                combatlog.text = combatlog.text[0:-1] + ':'
                thero, thero_two = thero_two, thero
            
            coefficient = TableExperience.objects.get(level=thero.level). \
                                                                    coefficient
            damage_bamp = 0
            i = 0
            for strike in strikes:
                accuracy = devastate = block = block_break = armor_break = \
                                                                isblock = False
                                
                if random.randint(0, accuracy_p) not in \
                                        range(int(thero.feature.accuracy) -
                                              int(thero_two.feature.dodge)):
                    accuracy = True
                    
                if random.randint(0, devastate_p) in \
                                    range(int(thero.feature.devastate) -
                                          int(thero_two.feature.durability)):
                    devastate = True
                
                if strike in blocks_two:
                    block = True
                    isblock = True
                    if random.randint(0, block_break_p) in \
                                        range(int(thero.feature.block_break)):
                        block_break = True
                        isblock = False
                
                if random.randint(0, armor_break_p) in \
                                        range(int(thero.feature.armor_break)):
                    armor_break = True
                     
                damage = random.randint(int(thero.feature.damage_min),
                                        int(thero.feature.damage_max))
                                        
                if strike == 1: 
                    protection = int(thero.feature.protection_breast)
                elif strike == 2: 
                    protection = int(thero.feature.protection_zone)
                elif strike == 3: 
                    protection = int(thero.feature.protection_legs)
                else: 
                    protection = int(thero.feature.protection_head)
                
                if not armor_break:
                    strike_damage = int(damage - damage * 
                                        (protection / damage_p / 100.0))
                else:
                    strike_damage = damage
                    
                if devastate:
                    strike_damage *= 2
                
                if isblock == True or not accuracy:
                    strike_damage = 0              
                        
                if strike_damage > 0:
                    current_hp = float(thero_two.feature.hp.split('|')[0])
                    current_hp -= strike_damage
                    if int(current_hp) <= 0:
                        current_hp = 0
                        combathero = combat.combathero_set.get(hero=thero_two)
                        combathero.is_dead = True
                        combathero.save()
                        dead_heroes.append({'hero': thero_two,
                                            'team': combathero.team})
                    
                    set_hp(thero_two, current_hp)    
                    
                strikes[i] = str(strike) + '_' + str(strike_damage) + '_' + \
                             str(int(block)) + '_' + str(int(block_break)) + \
                             '_' + str(int(not accuracy)) + '_' + \
                             str(int(devastate)) + '_' + str(int(armor_break))
                
                damage_bamp += strike_damage                                                                                                                                                                   
                combatlog.text += '[hero_one]' + str(thero) + \
                                  '[/hero_one][hero_two]' + str(thero_two) + \
                                  '[/hero_two][strikes]' + strikes[i] + \
                                  '[/strikes][blocks]' + \
                                  '|'.join(blocks_two) + '[/blocks]&'
                
                i += 1
                                                 
            strikes_s = '|'.join(strikes)
            blocks_s = '|'.join(blocks_two)
            
            if team == Combat.TEAM_FIRST:
                combatlog.hero_one_wstrike = strikes_s
                combatlog.hero_two_wblock = blocks_s 
                combatlog.hero_one_damage = damage_bamp
                combatlog.hero_one_experience = int(damage_bamp * coefficient)  
            else:
                combatlog.hero_two_wstrike = strikes_s
                combatlog.hero_one_wblock = blocks_s
                combatlog.hero_two_damage = damage_bamp
                combatlog.hero_two_experience = int(damage_bamp * coefficient)
        
        combatlog.is_past = True
        combatlog.text = combatlog.text[0:-1]
        
        combatlog.save()
        
        after_death(combat, dead_heroes)
        
def is_timeout(combat, team):

    count_in_team = combat.combathero_set.filter(team=team, is_dead=False). \
                                                                        count()
    count_in_not_answer_team = combat.combathero_set.filter(is_dead=False). \
                                                    exclude(team=team).count()
    datetime_limit = datetime.datetime.fromtimestamp(time.time() - \
                                                     combat.time_out)
    
    if team == Combat.TEAM_FIRST:
        count_not_answer = combat.combatlog_set.filter(hero_two_wstrike=None,
                                                       is_past=False,
                                                       is_dead=False,
                                                       is_start=False,
                                            time__lte=datetime_limit).count()
    else:
        count_not_answer = combat.combatlog_set.filter(hero_one_wstrike=None,
                                                       is_past=False,
                                                       is_dead=False,
                                                       is_start=False,
                                            time__lte=datetime_limit).count()
    return ((count_in_team * count_in_not_answer_team) - count_not_answer) == 0

def after_death(combat, dead_heroes):
    for dead_hero in dead_heroes:
        if dead_hero['team'] == Combat.TEAM_FIRST:
            combat.combatlog_set.filter(is_past=False,
                                        hero_one=dead_hero['hero']).delete()
        else:
            combat.combatlog_set.filter(is_past=False,
                                        hero_two=dead_hero['hero']).delete()
        write_log_messages(combat, is_dead=True, hero=dead_hero['hero'])
#End
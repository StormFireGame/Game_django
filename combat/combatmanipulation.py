from django.db.models import Q

from combat.models import Combat, CombatLog, CombatWarrior
from tableexperience.models import TableExperience
from hero.models import Hero
from bot.models import Bot

from hero.heromanipulation import set_hp

import time
import random
import datetime

def get_location(location):
    location = location.split('&')
    
    island_location = location[0].split('|')
    del island_location[2]
    location[0] = '|'.join(island_location)
    
    return '&'.join(location)

def in_combat(hero, is_active=Combat.IS_ACTIVE_WAIT):
    try:
        combat = Combat.objects.filter(combatwarrior__hero=hero, 
                                       is_active=is_active, 
                                       combatwarrior__is_quit=False).get()
        return combat
    except Combat.DoesNotExist:
        return False

def in_active_combat(hero):
    try:
        combat = Combat.objects.filter(Q(is_active=Combat.IS_ACTIVE_FIGHT) | 
                                    Q(is_active=Combat.IS_ACTIVE_AFTER_FIGHT),
                                       combatwarrior__hero=hero,
                                       combatwarrior__is_quit=False).get()
        return combat
    except Combat.DoesNotExist:
        return False
    
def is_cancel(hero):
    try:
        combat = Combat.objects.filter(combatwarrior__hero=hero, 
                                       is_active=Combat.IS_ACTIVE_WAIT).get()
        if combat.combatwarrior_set.count() == 1:
            return True
        else:
            return False
    except Combat.DoesNotExist:
        return False

def is_combat(hero):
    return in_active_combat(hero) != False

# For duel
def is_fight(hero):
    try:
        combat = \
            Combat.objects.filter(combatwarrior__hero=hero, 
                                  combatwarrior__team=Combat.TEAM_FIRST, 
                                  type=Combat.TYPE_DUEL, 
                                  is_active=Combat.IS_ACTIVE_WAIT).get()
        return combat.combatwarrior_set.count() == 2
    except Combat.DoesNotExist:
        return False

def is_refuse(hero):
    try:
        combat = Combat.objects.filter(combatwarrior__hero=hero, 
                                       type=Combat.TYPE_DUEL, 
                                       is_active=Combat.IS_ACTIVE_WAIT).get()
        if combat.combatwarrior_set.count() == 2:
            return combat
    except Combat.DoesNotExist:
        pass
    return False

def update_combats(type):
    combats = Combat.objects.filter(type=type, is_active=Combat.IS_ACTIVE_WAIT)
    
    for combat in combats:
        one_team_count = combat.combatwarrior_set. \
                                        filter(team=Combat.TEAM_FIRST).count()
        two_team_count = combat.combatwarrior_set. \
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
        
        count = combat.combatwarrior_set.count()
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
            
        combatwarriors = combat.combatwarrior_set.all()
        for i in to_replace:
            combatwarrior = combat.combatwarrior_set.get(
                                                    pk=combatwarriors[i].id)
            combatwarrior.team = Combat.TEAM_SECOND
            combatwarrior.save()
            
    combat.is_active = Combat.IS_ACTIVE_FIGHT
    combat.save()
# End

# Combat inside
def is_dead(combat, hero, bot=None):
    return combat.combatwarrior_set.filter(hero=hero, bot=bot, is_dead=True). \
                                                                    exists()

def is_draw(combat):
    return combat.combatwarrior_set.all().count() == \
                        combat.combatwarrior_set.filter(is_dead=True).count()
    
def is_win(combat, team, is_draw):
    return not combat.combatwarrior_set.filter(is_dead=False). \
                                exclude(team=team).exists() and not is_draw

def is_lose(combat, team, is_draw):
    return not combat.combatwarrior_set.filter(is_dead=False, team=team). \
                                                    exists() and not is_draw
                                                    
def get_enemies(combat, hero, team):
    if team == Combat.TEAM_FIRST:
        heroes = [ i.hero for i in combat.combatwarrior_set.
                                    filter(is_dead=False).exclude(team=team)
                    if not combat.combatlog_set.filter(hero_one=hero, 
                                                       hero_two=i.hero, 
                                                       is_past=False, 
                                                    warrior_two_wstrike=None) 
                                                       and i.hero ]  
    else:
        heroes = [ i.hero for i in combat.combatwarrior_set. \
                                    filter(is_dead=False).exclude(team=team) 
                    if not combat.combatlog_set.filter(hero_two=hero, 
                                                       hero_one=i.hero, 
                                                       is_past=False, 
                                                    warrior_one_wstrike=None) 
                                                       and i.hero ]
    
    
    bots = [ i.bot for i in combat.combatwarrior_set.filter(is_dead=False). \
                                                        exclude(team=team) 
                                                        if i.bot ] 
    
    return heroes + bots 

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

def get_combat_log(combat, hero, hero_two, bot, team):
    try:
        if team == Combat.TEAM_FIRST:
            return combat.combatlog_set.filter(hero_one=hero,
                                               hero_two=hero_two, bot_two=bot,
                                               is_past=False).get()
        else:
            return combat.combatlog_set.filter(hero_two=hero,
                                               hero_one=hero_two, bot_one=bot,
                                               is_past=False).get()
    except CombatLog.DoesNotExist:
        return None
                                                        
def write_log_message(combat, is_start=False, is_finish=False, win_team=None, 
                       is_dead=False, is_join=False, hero=None, bot=None):
    if is_start:
        if combat.combatlog_set.filter(is_start=True).exists():
            return
        
        warriors_one = []
        warriors_two = []
        for combatwarrior in combat.combatwarrior_set.all():
            if combatwarrior.team == Combat.TEAM_FIRST:
                if combatwarrior.hero:
                    warriors_one.append(str(combatwarrior.hero))
                else:
                    warriors_one.append(str(combatwarrior.bot))
            else:
                if combatwarrior.hero:
                    warriors_two.append(str(combatwarrior.hero))
                else:
                    warriors_two.append(str(combatwarrior.bot))
            
        combat.combatlog_set.create(is_start=True, \
                            text='[warriors_one]' + ','.join(warriors_one) + \
                                 '[/warriors_one]' + '[warriors_two]' + \
                                 ','.join(warriors_two) + '[/warriors_two]')
    
    if is_finish:
        if combat.combatlog_set.filter(is_finish=True).exists():
            return
    
        if win_team == None:
            warriors_one = []
            warriors_two = []
            for combatwarrior in combat.combatwarrior_set.all():
                if combatwarrior.team == Combat.TEAM_FIRST:
                    if combatwarrior.hero:
                        warriors_one.append(str(combatwarrior.hero))
                    else:
                        warriors_one.append(str(combatwarrior.bot))
                else:
                    if combatwarrior.hero:
                        warriors_two.append(str(combatwarrior.hero))
                    else:
                        warriors_two.append(str(combatwarrior.bot))
            
            combat.combatlog_set.create(is_finish=True, 
                            text='[warriors_one]' + ','.join(warriors_one) + \
                                 '[/warriors_one]' + '[warriors_two]' + \
                                 ','.join(warriors_two) + '[/warriors_two]')
        
        else:
            warriors = []
            for combatwarrior in combat.combatwarrior_set. \
                                                        filter(team=win_team):
                if combatwarrior.hero:
                    warriors.append(str(combatwarrior.hero))
                else:
                    warriors.append(str(combatwarrior.bot))
             
            combat.combatlog_set.create(is_finish=True,
                text='[warriors_one]' + ','.join(warriors) + '[/warriors_one]')
    
    if is_dead:
        warrior = hero if hero else bot
        combat.combatlog_set.create(is_dead=True, hero_one=hero, bot_one=bot,
                                text='[warrior]' + str(warrior) + '[/warrior]')
    if is_join:
        combat.combatlog_set.create(is_join=True, hero_one=hero, 
                                text='[warrior]' + str(hero) + '[/warrior]')

##
def write_log_strikes(combat, combatlog, team, hero, hero_two, bot, strikes, 
                      blocks):
    if combatlog is None:
        strikes_s = '|'.join(strikes)
        blocks_s = '|'.join(blocks)
     
        if team == Combat.TEAM_FIRST:
            tcombatlog = combat.combatlog_set.create(hero_one=hero,
                                                     hero_two=hero_two,
                                                     bot_two=bot,
                                                     is_past=False,
                                                warrior_one_wstrike=strikes_s,
                                                warrior_one_wblock=blocks_s)
        else:
            tcombatlog = combat.combatlog_set.create(hero_one=hero_two,
                                                     bot_one=bot,
                                                     hero_two=hero,
                                                     is_past=False,
                                                warrior_two_wstrike=strikes_s,
                                                warrior_two_wblock=blocks_s)
    
    if bot:
        combatlog = tcombatlog
    
    if combatlog:
        if hero_two:
            if team == Combat.TEAM_FIRST:
                strikes_two = combatlog.warrior_two_wstrike.split('|')
                blocks_two = combatlog.warrior_two_wblock.split('|')
            else:
                strikes_two = combatlog.warrior_one_wstrike.split('|')
                blocks_two = combatlog.warrior_one_wblock.split('|')
        
            warrior_two = hero_two
        else:
            strikes_two = [ str(random.randint(0, 3)) 
                                for i in range(int(bot.feature.strike_count)) ]
                        
            count_blocks = int(bot.feature.block_count)
            blocks_two = []
            i = 0
            while(True):
                block = str(random.randint(0, 3))
                if block not in blocks_two:
                    blocks_two.append(block)
                    i += 1
                if count_blocks == i:
                    break
            
            warrior_two = bot
        
        warrior = hero
          
        accuracy_p = 500
        devastate_p = 500
        block_break_p = 1000
        armor_break_p = 1000
        damage_p = 10
        
        dead_warriors = []
        combatlog.text = ''
        for j in range(2):
            if j == 1:
                strikes = strikes_two
                blocks_two = blocks
                team = int(not team)
                combatlog.text = combatlog.text[0:-1] + ':'
                warrior, warrior_two = warrior_two, warrior
            
            coefficient = TableExperience.objects. \
                                    get(level=warrior_two.level).coefficient
            damage_bamp = 0
            i = 0
            for strike in strikes:
                accuracy = devastate = block = block_break = armor_break = \
                                                            is_block = False
                                
                if random.randint(0, accuracy_p) not in \
                                        range(int(warrior.feature.accuracy) -
                                              int(warrior_two.feature.dodge)):
                    accuracy = True
                    
                if random.randint(0, devastate_p) in \
                                    range(int(warrior.feature.devastate) -
                                          int(warrior_two.feature.durability)):
                    devastate = True
                
                if strike in blocks_two:
                    block = True
                    is_block = True
                    if random.randint(0, block_break_p) in \
                                    range(int(warrior.feature.block_break)):
                        block_break = True
                        is_block = False
                
                if random.randint(0, armor_break_p) in \
                                    range(int(warrior.feature.armor_break)):
                    armor_break = True
                     
                damage = random.randint(int(warrior.feature.damage_min),
                                        int(warrior.feature.damage_max))
                                        
                if strike == 1: 
                    protection = int(warrior.feature.protection_breast)
                elif strike == 2: 
                    protection = int(warrior.feature.protection_zone)
                elif strike == 3: 
                    protection = int(warrior.feature.protection_legs)
                else: 
                    protection = int(warrior.feature.protection_head)
                
                if not armor_break:
                    strike_damage = int(damage - damage * 
                                        (protection / damage_p / 100.0))
                else:
                    strike_damage = damage
                    
                if devastate:
                    strike_damage *= 2
                
                if is_block == True or not accuracy:
                    strike_damage = 0              
                        
                if strike_damage > 0:
                    current_hp = int(float(warrior_two.feature.hp. \
                                                                split('|')[0]))
                    if current_hp != 0:
                        current_hp -= strike_damage
                        if int(current_hp) <= 0:
                            current_hp = 0
                            if type(warrior_two) == Hero:
                                combatwarrior = combat.combatwarrior_set.get(
                                                            hero=warrior_two)
                            else:
                                combatwarrior = combat.combatwarrior_set.get(
                                                            bot=warrior_two)
                            combatwarrior.is_dead = True
                            combatwarrior.save()
                            dead_warriors.append({'warrior': warrior_two,
                                                'team': combatwarrior.team})
                        
                        if type(warrior_two) == Hero:
                            set_hp(warrior_two, current_hp)
                        else:
                            warrior_two.feature.hp = '%s|%s' % (current_hp, 
                                        warrior_two.feature.hp.split('|')[1])
                            warrior_two.feature.save()    
                    
                strikes[i] = str(strike) + '_' + str(strike_damage) + '_' + \
                             str(int(block)) + '_' + str(int(block_break)) + \
                             '_' + str(int(not accuracy)) + '_' + \
                             str(int(devastate)) + '_' + str(int(armor_break))
                
                damage_bamp += strike_damage                                                                                                                                                                   
                combatlog.text += '[warrior_one]' + str(warrior) + \
                                  '[/warrior_one][warrior_two]' + \
                                str(warrior_two) + '[/warrior_two][strikes]' \
                                  + strikes[i] + '[/strikes][blocks]' + \
                                  '|'.join(blocks_two) + '[/blocks]&'
                
                i += 1
                                                 
            strikes_s = '|'.join(strikes)
            blocks_s = '|'.join(blocks_two)
            
            if team == Combat.TEAM_FIRST:
                combatlog.warrior_one_wstrike = strikes_s
                combatlog.warrior_two_wblock = blocks_s 
                combatlog.warrior_one_damage = damage_bamp
                combatlog.warrior_one_experience = \
                                                int(damage_bamp * coefficient)  
            else:
                combatlog.warrior_two_wstrike = strikes_s
                combatlog.warrior_one_wblock = blocks_s
                combatlog.warrior_two_damage = damage_bamp
                combatlog.warrior_two_experience = \
                                                int(damage_bamp * coefficient)
        
        combatlog.is_past = True
        combatlog.text = combatlog.text[0:-1]
        
        combatlog.save()
        
        after_death(combat, dead_warriors)
        
def is_timeout(combat, team, is_bot_call=False):

    count_in_team = combat.combatwarrior_set.filter(team=team, 
                                                    bot=None,
                                                    is_dead=False).count()
    if count_in_team and is_bot_call:
        return False
    
    count_in_not_answer_team = combat.combatwarrior_set. \
                                                    filter(is_dead=False). \
                                                    exclude(team=team).count()
    datetime_limit = datetime.datetime.fromtimestamp(time.time() - \
                                                     combat.time_out)
    
    if team == Combat.TEAM_FIRST:
        count_not_answer = combat.combatlog_set.filter(
                                                    warrior_two_wstrike=None,
                                                       is_past=False,
                                            time__lte=datetime_limit).count()
    else:
        count_not_answer = combat.combatlog_set.filter(
                                                    warrior_one_wstrike=None,
                                                       is_past=False,
                                            time__lte=datetime_limit).count()
    
    was_actions = combat.combatlog_set.filter((~Q(warrior_one_wstrike=None) &
                                              ~Q(warrior_two_wstrike=None)) |
                                               Q(is_start=True),
                                              time__gte=datetime_limit). \
                                                                    exists()
    
    all_worriors_not_answer = ((count_in_team * count_in_not_answer_team) - \
                                                        count_not_answer) == 0
    return (all_worriors_not_answer and not was_actions)

def after_death(combat, dead_warriors):
    for dead_warrior in dead_warriors:
        if dead_warrior['team'] == Combat.TEAM_FIRST:
            combat.combatlog_set.filter(is_past=False,
                                        hero_one=dead_warrior['warrior'], 
                                        bot_one=dead_warrior['warrior']). \
                                                                    delete()
        else:
            combat.combatlog_set.filter(is_past=False,
                                        hero_two=dead_warrior['warrior'],
                                        bot_two=dead_warrior['warrior']). \
                                                                    delete()
        is_warrior_hero = type(dead_warrior['warrior']) == Hero
        write_log_message(combat, is_dead=True, 
                hero=dead_warrior['warrior'] if is_warrior_hero else None, 
                bot=dead_warrior['warrior'] if not is_warrior_hero else None)
# Bots
def free_bots_from_combat(combat):
    for combatwarrior in combat.combatwarrior_set.exclude(bot=None):
        combatwarrior.is_quit = True
        combatwarrior.save()
        
        combatwarrior.bot.in_combat = False
        combatwarrior.bot.current_coordinate_x = \
                                random.randint(combatwarrior.bot.coordinate_x1, 
                                               combatwarrior.bot.coordinate_x2)
        combatwarrior.bot.current_coordinate_y = \
                                random.randint(combatwarrior.bot.coordinate_y1, 
                                               combatwarrior.bot.coordinate_y2)
        combatwarrior.bot.save()
        
        hp = combatwarrior.bot.feature.hp.split('|')
        hp[0] = hp[1]
        combatwarrior.bot.feature.hp = '|'.join(hp)
        combatwarrior.bot.feature.save()

def update_bots_timeout_in_combat(combat):
    
    try: 
        combatwarrior = combat.combatwarrior_set.filter(is_dead=False). \
                                                exclude(bot=None)[0:1].get()
        team = combatwarrior.team
        if is_timeout(combat, team, True):
            dead_warriors = []
            for combatwarrior in combat.combatwarrior_set. \
                                    filter(is_dead=False).exclude(team=team):
                set_hp(combatwarrior.hero, 0)
                combatwarrior.is_dead = True
                combatwarrior.save()
                dead_warriors.append({'warrior': combatwarrior.hero, 
                                      'team': combatwarrior.team})
    
            after_death(combat, dead_warriors)
            return True
    except CombatWarrior.DoesNotExist:
        return False
    
def update_bots_timeout(coordinate_x, coordinate_y):
    bots = Bot.objects.filter(coordinate_x1__lte=coordinate_x,
                              coordinate_y1__lte=coordinate_y, 
                              coordinate_x2__gte=coordinate_x, 
                              coordinate_y2__gte=coordinate_y, in_combat=True)
    
    for bot in bots:
        combat = Combat.objects.filter(combatwarrior__bot=bot, 
                                       combatwarrior__is_dead=False, 
                                       is_active=Combat.IS_ACTIVE_FIGHT).get()
        
        team = combat.combatwarrior_set.get(bot=bot).team
        
        if is_timeout(combat, team, True):
            dead_warriors = []
            for combatwarrior in combat.combatwarrior_set. \
                                    filter(is_dead=False).exclude(team=team):
                set_hp(combatwarrior.hero, 0)
                combatwarrior.is_dead = True
                combatwarrior.save()
                dead_warriors.append({'warrior': combatwarrior.hero, 
                                      'team': combatwarrior.team})
    
            after_death(combat, dead_warriors)
            
            free_bots_from_combat(combat)
# End    
# End
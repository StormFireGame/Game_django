from combat.models import Combat

import time
import random

def get_location(location):
    return location.split(':')[0]

def in_combat(hero, is_active=0):
    try:
        combat = \
            Combat.objects.filter(combathero__hero=hero, is_active=is_active) \
                                                                        .get()
        return combat
    except Combat.DoesNotExist:
        return False

def is_cancel(hero):
    try:
        combat = \
            Combat.objects.filter(combathero__hero=hero, is_active=0).get()
        if combat.combathero_set.count() == 1:
            return combat
        else:
            return False
    except Combat.DoesNotExist:
        return False

def is_fight(hero):
    try:
        combat = \
            Combat.objects.filter(combathero__hero=hero, combathero__team=0, 
                                  type=0, is_active=0).get()
        return combat.combathero_set.count() == 2
    except Combat.DoesNotExist:
        return False

def is_refuse(hero):
    try:
        combat = \
            Combat.objects.filter(combathero__hero=hero, type=0, is_active=0) \
                                                                        .get()
        if combat.combathero_set.count() == 2:
            return combat
    except Combat.DoesNotExist:
        pass
    return False

def is_combat(hero):
    combat = Combat.objects.filter(combathero__hero=hero) \
                                            .exclude(is_active=2, type=0).get()
    
    time_start = int(time.mktime(combat.start_date_time.timetuple()))
    if (int(time.time()) - time_start) >= combat.time_wait:
        combat.is_active = 1
        combat.save()
        return True
    
    combat.time_wait_left = combat.time_wait - (int(time.time()) - time_start)   
    combat.save()
    return False

def write_log(combat, combatlog, team, hero, hero_two, strikes, blocks):
    if combatlog is None:
        strikes_s = '|'.join(strikes)
        blocks_s = '|'.join(blocks)
     
        if team == 0:
            combatlog = combat.combatlog_set.create(hero_one=hero, hero_two=hero_two, hero_one_wstrike=strikes_s, hero_one_wblock=blocks_s)
        else:
            combatlog = combat.combatlog_set.create(hero_one=hero_two, hero_two=hero, hero_two_wstrike=strikes_s, hero_two_wblock=blocks_s)
    else:
        if team == 0:
            strikes_two = combatlog.hero_two_wstrike.split('|')
            blocks_two = combatlog.hero_two_wblock.split('|')
        else:
            strikes_two = combatlog.hero_one_wstrike.split('|')
            blocks_two = combatlog.hero_one_wblock.split('|')
   
        accuracy_p = 500
        devastate_p = 500
        block_break_p = 1000
        armor_break_p = 1000
        damage_p = 10
        
        combatlog.text = ''
        for j in range(2):
            if j == 1:
                strikes = strikes_two
                blocks_two = blocks
                team = int(not team)
                combatlog.text = combatlog.text[0:-1] + ':'
            
            i = 0
            for strike in strikes:
                accuracy = devastate = block = block_break = armor_break = False
                                
                if random.randint(0, accuracy_p) not in range(int(hero.feature.accuracy) - int(hero_two.feature.dodge)):
                    accuracy = True
                    
                if random.randint(0, devastate_p) in range(int(hero.feature.devastate) - int(hero_two.feature.durability)):
                    devastate = True
                
                isblock = True
                if strike in blocks_two:
                    block = True
                    if random.randint(0, block_break_p) in range(int(hero.feature.block_break)):
                        block_break = True
                        isblock = False
                
                if random.randint(0, armor_break_p) in range(int(hero.feature.armor_break)):
                        armor_break = True
                     
                damage = random.randint(int(hero.feature.damage_min), int(hero.feature.damage_max))
                                        
                if strike == 1: protection = int(hero.feature.protection_head)
                elif strike == 2: protection = int(hero.feature.protection_head)
                elif strike == 3: protection = int(hero.feature.protection_head)
                else: protection = int(hero.feature.protection_head)
                
                if not armor_break:
                    strike_damage = int(damage - damage * (protection / damage_p / 100.0))
                else:
                    strike_damage = damage
                    
                if devastate:
                    strike_damage *= 2
                
                if isblock == True or accuracy:
                    strike_damage = 0
                
                strikes[i] = str(strike) + '_' + str(strike_damage) + '_' + str(int(block)) + '_' + str(int(block_break)) + '_' + str(int(not accuracy)) + '_' + str(int(devastate)) + '_' + str(int(armor_break))
                                                                                                                                                                                            
                if team == 0:
                    combatlog.text += '[hero_one]' + str(hero) + '[/hero_one][hero_two]' + str(hero_two) + '[/hero_two][strike]' + strikes[i] + '[/strike][block]' + '|'.join(blocks_two) + '[/block]|'
                else:
                    combatlog.text += '[hero_one]' + str(hero_two) + '[/hero_one][hero_two]' + str(hero) + '[/hero_two][strike]' + strikes[i] + '[/strike][block]' + '|'.join(blocks_two) + '[/block]|'
                
                i += 1
                                                 
            strikes_s = '|'.join(strikes)
            blocks_s = '|'.join(blocks_two)
            
            if team == 0:
                combatlog.hero_one_wstrike = strikes_s
                combatlog.hero_two_wblock = blocks_s             
            else:
                combatlog.hero_two_wstrike = strikes_s
                combatlog.hero_one_wblock = blocks_s   
        
        combatlog.is_past = True
        combatlog.text = combatlog.text[0:-1]
        
        combatlog.save()
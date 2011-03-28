from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from tableexperience.models import TableExperience
from hero.models import Hero
from thing.models import Thing

import time 

def hero_init(origin_func):
    def inner_decorator(request, *args, **kwargs):
        if 'hero_id' not in request.session:
#
            messages.add_message(request, messages.ERROR,
                                 'You have to log in.')
            return HttpResponseRedirect('/')
        try:
            hero = Hero.objects.get(id=request.session['hero_id'])
        except Hero.DoesNotExist:
            return HttpResponseRedirect('/')
        
        from combat.combatmanipulation import is_combat
       
        request.hero = hero
        if not is_combat(hero):
            _hp(hero)
        else:
            if request.path != reverse('combat') and \
               request.path != reverse('combat_quit') and \
               request.path != reverse('combat_victory'):
                return HttpResponseRedirect(reverse('combat'))

        return origin_func(request, *args, **kwargs)
    return inner_decorator

##
def _hp(hero):
    hp = hero.feature.hp.split('|')
    current_time = float(hp[2])
    max_hp = int(hp[1])
    if max_hp == int(float(hp[0])):
        return
    one_hp_sec = 1500.0 / max_hp
    current_hp = float(hp[0]) + (time.time() - current_time) / one_hp_sec
    if current_hp > max_hp:
        current_hp = max_hp
    
    hero.feature.hp = '%s|%s|%s' % (current_hp, max_hp, time.time())
    hero.feature.save()

##
def _feature_help(hero, feature):
    if feature == Hero.FEATURE_DAMAGE_MIN:
        result = _plus_features(hero.feature.damage_min, \
                                int(hero.feature.strength) * 2)
    elif feature == Hero.FEATURE_DAMAGE_MAX:
        result = _plus_features(hero.feature.damage_max, \
                                int(hero.feature.strength) * 3)
    elif feature == Hero.FEATURE_ACCURACY:
        result = _plus_features(hero.feature.accuracy, \
                                int(hero.feature.dexterity) * 2)
    elif feature == Hero.FEATURE_DODGE:
        result = _plus_features(hero.feature.dodge, \
                                int(hero.feature.dexterity) * 2.5)
    elif feature == Hero.FEATURE_DEVASTATE:
        result = _plus_features(hero.feature.devastate, \
                                int(hero.feature.intuition) * 2.5)
    elif feature == Hero.FEATURE_DURABILITY:
        result = _plus_features(hero.feature.durability, \
                                int(hero.feature.intuition) * 2)
    elif feature == Hero.FEATURE_HP:
        hp = hero.feature.hp.split('|')
        hp[1] = _plus_features(hp[1], int(hero.feature.health) * 10)
        if not hero.id:
            hp[0] = hp[1]
        result = '|'.join(hp)
    
    elif feature == Hero.FEATURE_CAPACITY:
        capacity = hero.feature.capacity.split('|')
        capacity[1] = _plus_features(capacity[1], 
                                     int(hero.feature.strength) * 10)
        result = '|'.join(capacity)
       
    return result

def _featureskill_help(hero, skill, feature, plus):
    if feature == Hero.FEATURE_STRENGTH:
        hero.feature.strength = _plus_features(hero.feature.strength, 
                        plus * hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_DEXTERITY:
        hero.feature.dexterity = _plus_features(hero.feature.dexterity, 
                        plus * hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_INTUITION:
        hero.feature.intuition = _plus_features(hero.feature.intuition, 
                        plus * hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_HEALTH:
        hero.feature.health = _plus_features(hero.feature.health, 
                        plus * hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == Hero.FEATURE_SWORDS:
        hero.feature.swords = _plus_features(hero.feature.swords, 
                        plus * hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_AXES:
        hero.feature.axes = _plus_features(hero.feature.axes, 
                        plus * hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_KNIVES:
        hero.feature.knives = _plus_features(hero.feature.knives, 
                        plus * hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_CLUBS:
        hero.feature.clubs = _plus_features(hero.feature.clubs, 
                        plus * hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_SHIELDS:
        hero.feature.shields = _plus_features(hero.feature.shields, 
                        plus * hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == Hero.FEATURE_PROTECTION_HEAD:
        hero.feature.protection_head = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_PROTECTION_BREAST:
        hero.feature.protection_breast = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_PROTECTION_ZONE:
        hero.feature.protection_zone = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_PROTECTION_LEGS:
        hero.feature.protection_legs = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == Hero.FEATURE_DAMAGE_MIN:
        hero.feature.damage_min = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_DAMAGE_MAX:
        hero.feature.damage_max = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)        
    elif feature == Hero.FEATURE_ACCURACY:
        hero.feature.accuracy = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_DODGE:
        hero.feature.dodge = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_DEVASTATE:
        hero.feature.devastate = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_DURABILITY:
        hero.feature.durability = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_BLOCK_BREAK:
        hero.feature.block_break = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == Hero.FEATURE_ARMOR_BREAK:
        hero.feature.armor_break = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
                                
    elif feature == Hero.FEATURE_HP:
        hp = hero.feature.hp.split('|')
        hp[1] = str(plus * hero.heroheroskill_set.get(skill=skill).level)
        hero.feature.hp = '|'.join(hp)
        
    elif feature == Hero.FEATURE_CAPACITY:
        capacity = hero.feature.capacity.split('|')
        capacity[1] = str(plus * hero.heroheroskill_set.get(skill=skill).level)
        hero.feature.capacity = '|'.join(capacity)

def _featurething_help(hero, thing):
    hero.feature.strength = _plus_features(hero.feature.strength, 
                                           thing.strength_give)
    hero.feature.dexterity = _plus_features(hero.feature.dexterity, 
                                            thing.dexterity_give)
    hero.feature.intuition = _plus_features(hero.feature.intuition, 
                                            thing.intuition_give)
    hero.feature.health = _plus_features(hero.feature.health, 
                                         thing.health_give)
                
    hero.feature.swords = _plus_features(hero.feature.swords, 
                                         thing.swords_give)
    hero.feature.axes = _plus_features(hero.feature.axes, thing.axes_give)
    hero.feature.knives = _plus_features(hero.feature.knives, 
                                         thing.knives_give)
    hero.feature.clubs = _plus_features(hero.feature.clubs, thing.clubs_give)
    hero.feature.shields = _plus_features(hero.feature.shields, 
                                          thing.shields_give)
    
    hero.feature.damage_min = _plus_features(hero.feature.damage_min, 
                                             thing.damage_min)
    hero.feature.damage_max = _plus_features(hero.feature.damage_max, 
                                             thing.damage_max)
    
    hero.feature.protection_head = _plus_features(hero.feature.protection_head, 
                                                  thing.protection_head)
    hero.feature.protection_breast = \
                                _plus_features(hero.feature.protection_breast, 
                                               thing.protection_breast)
    hero.feature.protection_zone = _plus_features(hero.feature.protection_zone, 
                                                  thing.protection_zone)
    hero.feature.protection_legs = _plus_features(hero.feature.protection_legs, 
                                                 thing.protection_legs)
    
    hero.feature.accuracy = _plus_features(hero.feature.accuracy, 
                                           thing.accuracy)
    hero.feature.dodge = _plus_features(hero.feature.dodge, thing.dodge)
    hero.feature.devastate = _plus_features(hero.feature.devastate, 
                                         thing.devastate)
    hero.feature.durability = _plus_features(hero.feature.durability, 
                                             thing.durability)
    hero.feature.block_break = _plus_features(hero.feature.block_break, 
                                              thing.block_break)
    hero.feature.armor_break = _plus_features(hero.feature.armor_break, 
                                              thing.armor_break)
    
    if thing.hp:
        hp = hero.feature.hp.split('|')
        hp[1] = _plus_features(hp[1], thing.hp)
        hero.feature.hp = '|'.join(hp)
    
    hero.feature.strike_count = _plus_features(hero.feature.strike_count, 
                                               thing.strike_count)
    hero.feature.block_count = _plus_features(hero.feature.block_count, 
                                              thing.block_count)
    
    if thing.capacity:
        capacity = hero.feature.capacity.split('|')
        capacity[1] = _plus_features(capacity[1], thing.capacity)
        hero.feature.capacity = '|'.join(capacity)
        
    if thing.type == Thing.TYPE_SHIELD:
        hero.feature.block_count = _plus_features(hero.feature.block_count, 1)

def _featureherothing_help(hero, feature, plus):
    if feature == Hero.FEATURE_STRENGTH:
        hero.feature.strength = _plus_features(hero.feature.strength, plus)
    elif feature == Hero.FEATURE_DEXTERITY:
        hero.feature.dexterity = _plus_features(hero.feature.dexterity, plus)
    elif feature == Hero.FEATURE_INTUITION:
        hero.feature.intuition = _plus_features(hero.feature.intuition, plus)
    elif feature == Hero.FEATURE_HEALTH:
        hero.feature.health = _plus_features(hero.feature.health, plus)
    
    elif feature == Hero.FEATURE_SWORDS:
        hero.feature.swords = _plus_features(hero.feature.swords, plus)
    elif feature == Hero.FEATURE_AXES:
        hero.feature.axes = _plus_features(hero.feature.axes, plus)
    elif feature == Hero.FEATURE_KNIVES:
        hero.feature.knives = _plus_features(hero.feature.knives, plus)
    elif feature == Hero.FEATURE_CLUBS:
        hero.feature.clubs = _plus_features(hero.feature.clubs, plus)
    elif feature == Hero.FEATURE_SHIELDS:
        hero.feature.shields = _plus_features(hero.feature.shields, plus)
    
    elif feature == Hero.FEATURE_PROTECTION_HEAD:
        hero.feature.protection_head = \
                            _plus_features(hero.feature.protection_head, plus)
    elif feature == Hero.FEATURE_PROTECTION_BREAST:
        hero.feature.protection_breast = \
                        _plus_features(hero.feature.protection_breast, plus)
    elif feature == Hero.FEATURE_PROTECTION_ZONE:
        hero.feature.protection_zone = \
                            _plus_features(hero.feature.protection_zone, plus)
    elif feature == Hero.FEATURE_PROTECTION_LEGS:
        hero.feature.protection_legs = \
                            _plus_features(hero.feature.protection_legs, plus)
    
    elif feature == Hero.FEATURE_DAMAGE_MIN:
        hero.feature.damage_min = _plus_features(hero.feature.damage_min, plus)
    elif feature == Hero.FEATURE_DAMAGE_MAX:
        hero.feature.damage_max = _plus_features(hero.feature.damage_max, plus) 
    elif feature == Hero.FEATURE_ACCURACY:
        hero.feature.accuracy = _plus_features(hero.feature.accuracy, plus)
    elif feature == Hero.FEATURE_DODGE:
        hero.feature.dodge = _plus_features(hero.feature.dodge, plus)
    elif feature == Hero.FEATURE_DEVASTATE:
        hero.feature.devastate = _plus_features(hero.feature.devastate, plus)
    elif feature == Hero.FEATURE_DURABILITY:
        hero.feature.durability = _plus_features(hero.feature.durability, plus)
    elif feature == Hero.FEATURE_BLOCK_BREAK:
        hero.feature.block_break = _plus_features(hero.feature.block_break, 
                                                  plus)
    elif feature == Hero.FEATURE_ARMOR_BREAK:
        hero.feature.armor_break = _plus_features(hero.feature.armor_break, 
                                                  plus)
                                
    elif feature == Hero.FEATURE_HP:
        hp = hero.feature.hp.split('|')
        hp[1] = _plus_features(hp[1], plus)
        hero.feature.hp = '|'.join(hp)
        
    elif feature == Hero.FEATURE_CAPACITY:
        capacity = hero.feature.capacity.split('|')
        capacity[1] = _plus_features(capacity[1], plus)
        hero.feature.capacity = '|'.join(capacity)
    
    elif feature == Hero.FEATURE_STRIKE_COUNT:
        hero.feature.strike_count = _plus_features(hero.feature.strike_count, 
                                                   plus)
    elif feature == Hero.FEATURE_BLOCK_COUNT:
        hero.feature.block_count = _plus_features(hero.feature.block_count, 
                                                  plus)

def hero_feature(hero):
    hero.feature.strength = str(hero.strength)
    hero.feature.dexterity = str(hero.dexterity)
    hero.feature.intuition = str(hero.intuition)
    hero.feature.health = str(hero.health)
     
    hero.feature.swords = str(hero.swords)
    hero.feature.axes = str(hero.axes)
    hero.feature.knives = str(hero.knives)
    hero.feature.clubs = str(hero.clubs)
    hero.feature.shields = str(hero.shields)
    
    hero.feature.damage_min = hero.feature.damage_max = \
    hero.feature.accuracy = hero.feature.dodge = hero.feature.devastate = \
    hero.feature.durability = hero.feature.block_break = \
    hero.feature.armor_break = hero.feature.strike_count = \
    hero.feature.block_count = 0
    
    if hero.id:
        hero.feature.hp = '%s|%s|%s' % (hero.feature.hp.split('|')[0], 0, 
                                        time.time())
        hero.feature.capacity = '%s|%s' % (
                                    hero.feature.capacity.split('|')[0], 0)
    else:
        hero.feature.hp = '%s|%s|%s' % (0, 0, time.time())
        hero.feature.capacity = '0|0'
        
    hero.feature.strike_count = '1'
    hero.feature.block_count = '2'
    
    if hero.id:
        for skill in hero.skills.all():
            for skillfeature in skill.skillfeature_set.all():
                _featureskill_help(hero, skill, skillfeature.feature, 
                                   skillfeature.plus)
                
        count_of_arms = 0
        for herothing in hero.herothing_set.filter(dressed=True):
            _featurething_help(hero, herothing.thing)
            
            for herothingfeature in herothing.herothingfeature_set.all():
                _featureherothing_help(hero, herothingfeature.feature, 
                                   herothingfeature.plus)
            
            if herothing.thing.type == 0 or herothing.thing.type == 1 or \
               herothing.thing.type == 2 or herothing.thing.type == 3: 
                count_of_arms += 1;
                if count_of_arms == 2:
                    hero.feature.strike_count = \
                            _plus_features(hero.feature.strike_count, 1)
            
                             
    hero.feature.damage_min = _feature_help(hero, Hero.FEATURE_DAMAGE_MIN)
    hero.feature.damage_max = _feature_help(hero, Hero.FEATURE_DAMAGE_MAX)
    hero.feature.accuracy = _feature_help(hero, Hero.FEATURE_ACCURACY)
    hero.feature.dodge = _feature_help(hero, Hero.FEATURE_DODGE)
    hero.feature.devastate = _feature_help(hero, Hero.FEATURE_DEVASTATE)
    hero.feature.durability = _feature_help(hero, Hero.FEATURE_DURABILITY)
    hero.feature.hp = _feature_help(hero, Hero.FEATURE_HP)
    hero.feature.capacity =_feature_help(hero, Hero.FEATURE_CAPACITY)
    
    hero.feature.save()

def hero_level_up(hero):
    if hero.id:
        try:
            tableexperience = TableExperience.objects. \
                                    exclude(experience__gte=hero.experience)[0]
        except IndexError:
            return
            
        if hero.level < tableexperience.level:
            hero.number_of_abilities += tableexperience.number_of_abilities
            hero.number_of_skills += tableexperience.number_of_skills
            hero.number_of_parameters += tableexperience.number_of_parameters
            hero.money += tableexperience.money
            hero.level += 1
    else:
        tableexperience = TableExperience.objects.get(experience=0)
        
        hero.number_of_abilities += tableexperience.number_of_abilities
        hero.number_of_skills += tableexperience.number_of_skills
        hero.number_of_parameters += tableexperience.number_of_parameters
        hero.money += tableexperience.money   

def set_hp(hero, hp=-1):
    if hp == -1:
        hp = hero.feature.hp.split('|')[0]
    hero.feature.hp = '%s|%s|%s' % (hp, hero.feature.hp.split('|')[1], \
                                    time.time())
    hero.feature.save()

def update_capacity(hero):
    all_weight = 0
    for herothing in hero.herothing_set.filter(away=False):
        all_weight += herothing.thing.weight
    
    hero_capacity = hero.feature.capacity.split('|')
    hero_capacity[0] = str(all_weight)
    hero.feature.capacity = '|'.join(hero_capacity)
    hero.feature.save()

def _plus_features(hero_feature, other_feature):
    if other_feature:
        return str(int(hero_feature) + int(round(other_feature)))
    return hero_feature
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from hero.models import FEATURES
from tableexperience.models import TableExperience
from hero.models import Hero

import time 

def hero_init(origin_func):
    def inner_decorator(request, *args, **kwargs):
        if 'hero_id' not in request.session:
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

def _hp(hero):
    hp = hero.feature.hp.split('|')
    current_time = float(hp[2])
    max_hp = int(hp[1])
    if max_hp == int(float(hp[0])):
        return
    one_hp_sec = 1500 / max_hp
    current_hp = float(hp[0]) + (time.time() - current_time) / one_hp_sec
    if current_hp > max_hp:
        current_hp = max_hp
    
    hero.feature.hp = '%s|%s|%s' % (current_hp, max_hp, time.time())
    hero.feature.save()

##
def _feature_help(hero, feature):
    if feature == 'damage_min':
        result = int(round(int(hero.feature.damage_min) +
                           int(hero.feature.strength) * 2))
    elif feature == 'damage_max':
        result = int(round(int(hero.feature.damage_max) +
                           int(hero.feature.strength) * 3))
    elif feature == 'accuracy':
        result = int(round(int(hero.feature.accuracy) +
                           int(hero.feature.dexterity) * 2))
    elif feature == 'dodge':
        result = int(round(int(hero.feature.dodge) +
                           int(hero.feature.dexterity) * 2.5))
    elif feature == 'devastate':
        result = int(round(int(hero.feature.devastate) +
                           int(hero.feature.intuition) * 2.5))
    elif feature == 'durability':
        result = int(round(int(hero.feature.durability) +
                           int(hero.feature.intuition) * 2))
    elif feature == 'hp':
        if hero.id:
            current_hp = hero.feature.hp.split('|')[0]
            max_hp = int(hero.feature.hp.split('|')[1]) + \
                     int(hero.feature.health) * 10
            current_time = hero.feature.hp.split('|')[2]
        else:
            current_hp = max_hp = int(hero.feature.health) * 10
            current_time = time.time()
        
        result = '%s|%s|%s' % (current_hp, max_hp, current_time)
    elif feature == 'capacity':
        result = int(round(int(hero.feature.capacity) +
                           int(hero.feature.strength) * 10))
    
    return result

def _featureskill_help(hero, skill, feature, plus):
    if feature == 'Strength':
        hero.feature.strength = str(int(hero.feature.strength) + plus * 
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Dexterity':
        hero.feature.dexterity = str(int(hero.feature.dexterity) + plus * 
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == 'Intuition':
        hero.feature.intuition = str(int(hero.feature.intuition) + plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == 'Health':
        hero.feature.health = str(int(hero.feature.health) + plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == 'Swords':
        hero.feature.swords = str(int(hero.feature.swords) + plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Axes':
        hero.feature.axes = str(int(hero.feature.axes) + plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Knives':
        hero.feature.knives = str(int(hero.feature.knives) + plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Clubs':
        hero.feature.clubs = str(int(hero.feature.clubs) + plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Shields':
        hero.feature.shields = str(int(hero.feature.shields) + plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == 'Protection head':
        hero.feature.protection_head = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Protection breast':
        hero.feature.protection_breast = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Protection zone':
        hero.feature.protection_zone = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Protection leg':
        hero.feature.protection_leg = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == 'Damage min':
        hero.feature.damage_min = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Damage max':
        hero.feature.damage_max = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)        
    elif feature == 'Accuracy':
        hero.feature.accuracy = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Dodge':
        hero.feature.dodge = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Devastate':
        hero.feature.devastate = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Durability':
        hero.feature.durability = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Block break':
        hero.feature.block_break = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Armor break':
        hero.feature.armor_break = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)
                                
    elif feature == 'Hp':
        current_hp = hero.feature.hp.split('|')[0]
        current_time = hero.feature.hp.split('|')[2]
        hero.feature.hp = '%s|%s|%s' % (current_hp, plus *
                            hero.heroheroskill_set.get(skill=skill).level, 
                            current_time)
    elif feature == 'Capacity':
        hero.feature.capacity = str(plus *
                                hero.heroheroskill_set.get(skill=skill).level)

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
        hero.feature.durability = hero.feature.capacity = 0
        
        if hero.id:
            hero.feature.hp = '%s|%s|%s' % (hero.feature.hp.split('|')[0], 0, 
                                            time.time())
        
        hero.feature.strike_count = '1'
        hero.feature.block_count = '2'
        
        if hero.id:
            for skill in hero.skills.all():
                for skillfeature in skill.skillfeature_set.all():
                    _featureskill_help(hero, skill, 
                                       FEATURES[skillfeature.feature][1], 
                                       skillfeature.plus)
        
        hero.feature.damage_min = str(_feature_help(hero, 'damage_min'))
        hero.feature.damage_max = str(_feature_help(hero, 'damage_max'))
        hero.feature.accuracy = str(_feature_help(hero, 'accuracy'))
        hero.feature.dodge = str(_feature_help(hero, 'dodge'))
        hero.feature.devastate = str(_feature_help(hero, 'devastate'))
        hero.feature.durability = str(_feature_help(hero, 'durability'))
        hero.feature.hp = str(_feature_help(hero, 'hp'))
        hero.feature.capacity = str(_feature_help(hero, 'capacity')) + '/0'
        
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
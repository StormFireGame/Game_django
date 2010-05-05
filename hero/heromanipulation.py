from hero.models import HeroFeature, FEATURES
from tableexperience.models import TableExperience
    
def _feature_help(hero, feature):
    if feature == 'damage_min':
        result = int(hero.feature.damage_min) + \
                                    int(hero.feature.strength) * 2
    elif feature == 'damage_max':
        result = int(hero.feature.damage_max) + \
                            int(hero.feature.strength) * 3
    elif feature == 'accuracy':
        result = int(hero.feature.accuracy) + \
                            int(hero.feature.dexterity) * 2
    elif feature == 'dodge':
        result = int(hero.feature.dodge) + \
                            int(hero.feature.dexterity) * 2.5
    elif feature == 'devastate':
        result = int(hero.feature.devastate) + \
                            int(hero.feature.intuition) * 2.5
    elif feature == 'durability':
        result = int(hero.feature.durability) + \
                            int(hero.feature.intuition) * 2   
    elif feature == 'hp':
        result = int(hero.feature.hp) + \
                            int(hero.feature.health) * 10
    elif feature == 'capacity':
        result = int(hero.feature.capacity) + \
                            int(hero.feature.strength) * 10
    
    return int(round(result))

def _featureskill_help(hero, skill, feature, plus):
    if feature == 'Strength':
        hero.feature.strength = str(int(hero.feature.strength) + plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Dexterity':
        hero.feature.dexterity = str(int(hero.feature.dexterity) + plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == 'Intuition':
        hero.feature.intuition = str(int(hero.feature.intuition) + plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == 'Health':
        hero.feature.health = str(int(hero.feature.health) + plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == 'Swords':
        hero.feature.swords = str(int(hero.feature.swords) + plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Axes':
        hero.feature.axes = str(int(hero.feature.axes) + plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Knives':
        hero.feature.knives = str(int(hero.feature.knives) + plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Clubs':
        hero.feature.clubs = str(int(hero.feature.clubs) + plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Shields':
        hero.feature.shields = str(int(hero.feature.shields) + plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == 'Protection head':
        hero.feature.protection_head = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Protection breast':
        hero.feature.protection_breast = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Protection zone':
        hero.feature.protection_zone = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Protection leg':
        hero.feature.protection_leg = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    
    elif feature == 'Damage min':
        hero.feature.damage_min = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Damage max':
        hero.feature.damage_max = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)        
    elif feature == 'Accuracy':
        hero.feature.accuracy = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Dodge':
        hero.feature.dodge = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Devastate':
        hero.feature.devastate = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Durability':
        hero.feature.durability = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Block break':
        hero.feature.block_break = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Armor break':
        hero.feature.armor_break = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
                                
    elif feature == 'Hp':
        hero.feature.hp = str(plus * \
                                hero.heroheroskill_set.get(skill=skill).level)
    elif feature == 'Capacity':
        hero.feature.capacity = str(plus * \
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
        hero.feature.durability = hero.feature.hp = hero.feature.capacity = 0
        
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
            pass
    else:
        tableexperience = TableExperience.objects.get(experience=0)
        
        hero.number_of_abilities += tableexperience.number_of_abilities
        hero.number_of_skills += tableexperience.number_of_skills
        hero.number_of_parameters += tableexperience.number_of_parameters
        hero.money += tableexperience.money
    return hero
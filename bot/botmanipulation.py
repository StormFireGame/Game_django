from bot.models import Bot
from thing.models import Thing

def bot_feature(bot):
        bot.feature.strength = str(bot.strength)
        bot.feature.dexterity = str(bot.dexterity)
        bot.feature.intuition = str(bot.intuition)
        bot.feature.health = str(bot.health)
         
        bot.feature.swords = str(bot.swords)
        bot.feature.axes = str(bot.axes)
        bot.feature.knives = str(bot.knives)
        bot.feature.clubs = str(bot.clubs)
        bot.feature.shields = str(bot.shields)
        
        bot.feature.damage_min = bot.feature.damage_max = \
        bot.feature.accuracy = bot.feature.dodge = bot.feature.devastate = \
        bot.feature.durability = bot.feature.block_break = \
        bot.feature.armor_break = bot.feature.strike_count = \
        bot.feature.block_count = 0
        
        bot.feature.strike_count = '1'
        bot.feature.block_count = '2'
        
        bot.feature.hp = '%s|%s' % (0, 0)
    
        count_of_arms = 0
        for thing in bot.things.all():
            _featurething_help(bot, thing)
            
            if thing.thing.type == 0 or thing.thing.type == 1 or \
               thing.thing.type == 2 or thing.thing.type == 3: 
                count_of_arms += 1;
                if count_of_arms == 2:
                    bot.feature.strike_count = \
                            _plus_features(bot.feature.strike_count, 1)
            
                                 
        bot.feature.damage_min = _feature_help(bot, bot.FEATURE_DAMAGE_MIN)
        bot.feature.damage_max = _feature_help(bot, bot.FEATURE_DAMAGE_MAX)
        bot.feature.accuracy = _feature_help(bot, bot.FEATURE_ACCURACY)
        bot.feature.dodge = _feature_help(bot, bot.FEATURE_DODGE)
        bot.feature.devastate = _feature_help(bot, bot.FEATURE_DEVASTATE)
        bot.feature.durability = _feature_help(bot, bot.FEATURE_DURABILITY)
        bot.feature.hp = _feature_help(bot, bot.FEATURE_HP)
        
        bot.feature.save()

##
def _feature_help(bot, feature):
    if feature == Bot.FEATURE_DAMAGE_MIN:
        result = _plus_features(bot.feature.damage_min, \
                                int(bot.feature.strength) * 2)
    elif feature == Bot.FEATURE_DAMAGE_MAX:
        result = _plus_features(bot.feature.damage_max, \
                                int(bot.feature.strength) * 3)
    elif feature == Bot.FEATURE_ACCURACY:
        result = _plus_features(bot.feature.accuracy, \
                                int(bot.feature.dexterity) * 2)
    elif feature == Bot.FEATURE_DODGE:
        result = _plus_features(bot.feature.dodge, \
                                int(bot.feature.dexterity) * 2.5)
    elif feature == Bot.FEATURE_DEVASTATE:
        result = _plus_features(bot.feature.devastate, \
                                int(bot.feature.intuition) * 2.5)
    elif feature == Bot.FEATURE_DURABILITY:
        result = _plus_features(bot.feature.durability, \
                                int(bot.feature.intuition) * 2)
    elif feature == Bot.FEATURE_HP:
        hp = bot.feature.hp.split('|')
        hp[1] = _plus_features(hp[1], int(bot.feature.health) * 10)
        hp[0] = hp[1]
        result = '|'.join(hp)
    
    return result

def _featurething_help(bot, thing):
    bot.feature.strength = _plus_features(bot.feature.strength, 
                                          thing.strength_give)
    bot.feature.dexterity = _plus_features(bot.feature.dexterity, 
                                           thing.dexterity_give)
    bot.feature.intuition = _plus_features(bot.feature.intuition, 
                                           thing.intuition_give)
    bot.feature.health = _plus_features(bot.feature.health, thing.health_give)
                
    bot.feature.swords = _plus_features(bot.feature.swords, thing.swords_give)
    bot.feature.axes = _plus_features(bot.feature.axes, thing.axes_give)
    bot.feature.knives = _plus_features(bot.feature.knives, thing.knives_give)
    bot.feature.clubs = _plus_features(bot.feature.clubs, thing.clubs_give)
    bot.feature.shields = _plus_features(bot.feature.shields, 
                                         thing.shields_give)
    
    bot.feature.damage_min = _plus_features(bot.feature.damage_min, 
                                            thing.damage_min)
    bot.feature.damage_max = _plus_features(bot.feature.damage_max, 
                                            thing.damage_max)
    
    bot.feature.protection_head = _plus_features(bot.feature.protection_head, 
                                                 thing.protection_head)
    bot.feature.protection_breast = \
                                _plus_features(bot.feature.protection_breast, 
                                               thing.protection_breast)
    bot.feature.protection_zone = _plus_features(bot.feature.protection_zone, 
                                                 thing.protection_zone)
    bot.feature.protection_legs = _plus_features(bot.feature.protection_legs, 
                                                 thing.protection_legs)
    
    bot.feature.accuracy = _plus_features(bot.feature.accuracy, thing.accuracy)
    bot.feature.dodge = _plus_features(bot.feature.dodge, thing.dodge)
    bot.feature.devastate = _plus_features(bot.feature.devastate, 
                                         thing.devastate)
    bot.feature.durability = _plus_features(bot.feature.durability, 
                                             thing.durability)
    bot.feature.block_break = _plus_features(bot.feature.block_break, 
                                              thing.block_break)
    bot.feature.armor_break = _plus_features(bot.feature.armor_break, 
                                              thing.armor_break)
    
    if thing.hp:
        hp = bot.feature.hp.split('|')
        hp[1] = _plus_features(hp[1], thing.hp)
        bot.feature.hp = '|'.join(hp)
    
    bot.feature.strike_count = _plus_features(bot.feature.strike_count, 
                                               thing.strike_count)
    bot.feature.block_count = _plus_features(bot.feature.block_count, 
                                              thing.block_count)
    
    if thing.type == Thing.TYPE_SHIELD:
        bot.feature.block_count = _plus_features(bot.feature.block_count, 1)

def _plus_features(bot_feature, other_feature):
    if other_feature:
        return str(int(bot_feature) + int(round(other_feature)))
    return bot_feature
from django.conf import settings

from thing.models import Thing

class BotM:
    def __init__(self, bot):
        self.bot = bot

    def update_feature(self):
        bot_feature = self.bot.feature

        # Drop params
        bot_feature.strength = str(self.bot.strength)
        bot_feature.dexterity = str(self.bot.dexterity)
        bot_feature.intuition = str(self.bot.intuition)
        bot_feature.health = str(self.bot.health)

        bot_feature.swords = str(self.bot.swords)
        bot_feature.axes = str(self.bot.axes)
        bot_feature.knives = str(self.bot.knives)
        bot_feature.clubs = str(self.bot.clubs)
        bot_feature.shields = str(self.bot.shields)

        bot_feature.protection_head = bot_feature.protection_breast = \
        bot_feature.protection_zone = bot_feature.protection_legs = \
        bot_feature.damage_min = bot_feature.damage_max = \
        bot_feature.accuracy = bot_feature.dodge = bot_feature.devastate = \
        bot_feature.durability = bot_feature.block_break = \
        bot_feature.armor_break = bot_feature.strike_count = \
        bot_feature.block_count = 0

        bot_feature.strike_count = str(settings.BOT_CREATE_STRIKE_COUNT)
        bot_feature.block_count = str(settings.BOT_CREATE_BLOCK_COUNT)

        bot_feature.hp = '%s|%s' % (0, self.bot.hp)
        # End drop params

        # Things + params
        count_of_arms = 0
        for thing in self.bot.things.all():
            self.__featurething_help(thing)

            if thing.type == Thing.TYPE_SWORD or \
               thing.type == Thing.TYPE_AXE or \
               thing.type == Thing.TYPE_KNIVE or \
               thing.type == Thing.TYPE_CLUBS:
                count_of_arms += 1
                if count_of_arms == 2:
                    bot_feature.strike_count = \
                            self.__plus_features(bot_feature.strike_count, 1)
        # End things + params

        # Modifiers
        self.__modifiers_help()
        # End modifiers

        bot_feature.save()

    def __modifiers_help(self):
        bot_feature = self.bot.feature

        bot_feature.damage_min = self.__plus_features(bot_feature.damage_min,
                                                    int(bot_feature.strength) *
                                    settings.MODIFIER_COEFFICIENT_DAMAGE_MIN)
        bot_feature.damage_max = self.__plus_features(bot_feature.damage_max,
                                                    int(bot_feature.strength) *
                                    settings.MODIFIER_COEFFICIENT_DAMAGE_MAX)

        bot_feature.accuracy = self.__plus_features(bot_feature.accuracy,
                                                int(bot_feature.dexterity) *
                                        settings.MODIFIER_COEFFICIENT_ACCURACY)
        bot_feature.dodge = self.__plus_features(bot_feature.dodge,
                                                int(bot_feature.dexterity) *
                                        settings.MODIFIER_COEFFICIENT_DODGE)
        bot_feature.devastate = self.__plus_features(bot_feature.devastate,
                                                int(bot_feature.intuition) *
                                    settings.MODIFIER_COEFFICIENT_DEVASTATE)
        bot_feature.durability = self.__plus_features(bot_feature.durability,
                                                int(bot_feature.intuition) *
                                    settings.MODIFIER_COEFFICIENT_DURABILITY)

        hp = bot_feature.hp.split('|')
        hp[1] = self.__plus_features(hp[1], int(bot_feature.health) * 10)
        hp[0] = hp[1]
        bot_feature.hp = '|'.join(hp)

    def __featurething_help(self, thing):
        bot_feature = self.bot.feature
        
        bot_feature.strength = self.__plus_features(bot_feature.strength,
                                                    thing.strength_give)
        bot_feature.dexterity = self.__plus_features(bot_feature.dexterity,
                                                     thing.dexterity_give)
        bot_feature.intuition = self.__plus_features(bot_feature.intuition,
                                                     thing.intuition_give)
        bot_feature.health = self.__plus_features(bot_feature.health,
                                                  thing.health_give)

        bot_feature.swords = self.__plus_features(bot_feature.swords,
                                                  thing.swords_give)
        bot_feature.axes = self.__plus_features(bot_feature.axes,
                                                thing.axes_give)
        bot_feature.knives = self.__plus_features(bot_feature.knives,
                                                  thing.knives_give)
        bot_feature.clubs = self.__plus_features(bot_feature.clubs,
                                                 thing.clubs_give)
        bot_feature.shields = self.__plus_features(bot_feature.shields,
                                                   thing.shields_give)

        bot_feature.damage_min = self.__plus_features(bot_feature.damage_min,
                                                      thing.damage_min)
        bot_feature.damage_max = self.__plus_features(bot_feature.damage_max,
                                                      thing.damage_max)

        bot_feature.protection_head = \
                            self.__plus_features(bot_feature.protection_head,
                                                 thing.protection_head)
        bot_feature.protection_breast = \
                            self.__plus_features(bot_feature.protection_breast,
                                                 thing.protection_breast)
        bot_feature.protection_zone = \
                            self.__plus_features(bot_feature.protection_zone,
                                                 thing.protection_zone)
        bot_feature.protection_legs = \
                            self.__plus_features(bot_feature.protection_legs,
                                                 thing.protection_legs)

        bot_feature.accuracy = self.__plus_features(bot_feature.accuracy,
                                                    thing.accuracy)
        bot_feature.dodge = self.__plus_features(bot_feature.dodge,
                                                 thing.dodge)
        bot_feature.devastate = self.__plus_features(bot_feature.devastate,
                                                     thing.devastate)
        bot_feature.durability = self.__plus_features(bot_feature.durability,
                                                      thing.durability)

        bot_feature.block_break = self.__plus_features(bot_feature.block_break,
                                                       thing.block_break)
        bot_feature.armor_break = self.__plus_features(bot_feature.armor_break,
                                                       thing.armor_break)

        if thing.hp:
            hp = bot_feature.hp.split('|')
            hp[1] = self.__plus_features(hp[1], thing.hp)
            bot_feature.hp = '|'.join(hp)

        bot_feature.strike_count = \
                                self.__plus_features(bot_feature.strike_count,
                                                     thing.strike_count)
        bot_feature.block_count = self.__plus_features(bot_feature.block_count,
                                                       thing.block_count)

        if thing.type == Thing.TYPE_SHIELD:
            bot_feature.block_count = \
                            self.__plus_features(bot_feature.block_count, 1)
            
    def __plus_features(self, bot_feature, other_feature):
        if other_feature:
            return str(int(bot_feature) + int(round(other_feature)))
        return bot_feature

    def restore_hp(self):
        hp = self.bot.feature.hp.split('|')
        hp[0] = hp[1]
        self.bot.feature.hp = '|'.join(hp)
        self.bot.feature.save()
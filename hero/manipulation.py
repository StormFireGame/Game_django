from django.contrib import messages
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings

from hero.models import Hero
from thing.models import Thing
from island.models import Island
from tableexperience.models import TableExperience
from combat.models import Combat

import time

def hero_init(origin_func):
    def inner_decorator(request, *args, **kwargs):
        if 'hero_id' not in request.session:
#
            messages.add_message(request, messages.ERROR,
                                 'You have to log in.')
            return HttpResponseRedirect(reverse('main'))
        try:
            hero = Hero.objects.get(id=request.session['hero_id'])
        except Hero.DoesNotExist:
            return HttpResponseRedirect(reverse('main'))

        request.hero = hero

        from combat.manipulation import CombatM

        herom = HeroM(hero)
        combat = herom.get_combat()

        if combat and CombatM(combat, hero).is_active():
            if request.path != reverse('combat') and \
               request.path != reverse('combat_quit') and \
               request.path != reverse('combat_victory'):
                return HttpResponseRedirect(reverse('combat'))
        else:
            herom.update_hp()

        return origin_func(request, *args, **kwargs)
    return inner_decorator

def in_given_location(origin_func):
    def inner_decorator(request, *args, **kwargs):
        hero = request.hero

        if 'slug' in kwargs:
            slugs = [ i.split(':')[1] for i in hero.location.split('&')[1:] ]
            if not len(slugs) or kwargs['slug'] != slugs[-1]:
                return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))
        else:
            if len(hero.location.split('&')) > 1:
                return HttpResponseRedirect(reverse(settings.URL_REVERSE_404))

        return origin_func(request, *args, **kwargs)
    return inner_decorator

class HeroM:
    def __init__(self, hero):
        self.hero = hero

    def update_feature(self):

        # Drop params
        hero_feature = self.hero.feature
        
        hero_feature.strength = str(self.hero.strength)
        hero_feature.dexterity = str(self.hero.dexterity)
        hero_feature.intuition = str(self.hero.intuition)
        hero_feature.health = str(self.hero.health)

        hero_feature.swords = str(self.hero.swords)
        hero_feature.axes = str(self.hero.axes)
        hero_feature.knives = str(self.hero.knives)
        hero_feature.clubs = str(self.hero.clubs)
        hero_feature.shields = str(self.hero.shields)

        hero_feature.protection_head = hero_feature.protection_breast = \
        hero_feature.protection_zone = hero_feature.protection_legs = \
        hero_feature.damage_min = hero_feature.damage_max = \
        hero_feature.accuracy = hero_feature.dodge = hero_feature.devastate = \
        hero_feature.durability = hero_feature.block_break = \
        hero_feature.armor_break = 0

        hero_feature.strike_count = hero_feature.block_count = 0

        if self.hero.id:
            hero_feature.hp = '%s|%s|%s' % (hero_feature.hp.split('|')[0],
                                            self.hero.hp, time.time())
            hero_feature.capacity = '%s|%s' % (
                                        hero_feature.capacity.split('|')[0],
                                               self.hero.capacity)
        else:
            hero_feature.hp = '%s|%s|%s' % (0, self.hero.hp, time.time())
            hero_feature.capacity = '%s|%s' % (0, self.hero.capacity)

        hero_feature.strike_count = str(settings.HERO_CREATE_STRIKE_COUNT)
        hero_feature.block_count = str(settings.HERO_CREATE_BLOCK_COUNT)
        # End drop params

        if self.hero.id:
            # Skills + params
            for skill in self.hero.skills.all():
                for skillfeature in skill.skillfeature_set.all():
                    self.__featureskill_help(skill, skillfeature.feature,
                                             skillfeature.plus)
            # End skills + params

            # Things + params
            count_of_arms = 0
            for herothing in self.hero.herothing_set.filter(dressed=True):
                self.__featurething_help(herothing.thing)

                for herothingfeature in herothing.herothingfeature_set.all():
                    self.__featureherothing_help(herothingfeature.feature,
                                                 herothingfeature.plus)

                if herothing.thing.type == Thing.TYPE_SWORD or \
                   herothing.thing.type == Thing.TYPE_AXE or \
                   herothing.thing.type == Thing.TYPE_KNIVE or \
                   herothing.thing.type == Thing.TYPE_CLUBS:
                    count_of_arms += 1
                    if count_of_arms == settings.THINGS_COUNT_OF_ARMS:
                        hero_feature.strike_count = \
                            self.__plus_features(hero_feature.strike_count, 1)
            # End things + params

        # Modifiers
        self.__modifiers_help()
        # End modifiers

        hero_feature.save()

    def __modifiers_help(self):
        hero_feature = self.hero.feature

        hero_feature.damage_min = self.__plus_features(hero_feature.damage_min,
                                                int(hero_feature.strength) *
                                    settings.MODIFIER_COEFFICIENT_DAMAGE_MIN)
        hero_feature.damage_max = self.__plus_features(hero_feature.damage_max,
                                                int(hero_feature.strength) *
                                    settings.MODIFIER_COEFFICIENT_DAMAGE_MAX)

        hero_feature.accuracy = self.__plus_features(hero_feature.accuracy,
                                                int(hero_feature.dexterity) *
                                        settings.MODIFIER_COEFFICIENT_ACCURACY)
        hero_feature.dodge = self.__plus_features(hero_feature.dodge,
                                                int(hero_feature.dexterity) *
                                        settings.MODIFIER_COEFFICIENT_DODGE)
        hero_feature.devastate = self.__plus_features(hero_feature.devastate,
                                                int(hero_feature.intuition) *
                                    settings.MODIFIER_COEFFICIENT_DEVASTATE)
        hero_feature.durability = self.__plus_features(hero_feature.durability,
                                                int(hero_feature.intuition) *
                                    settings.MODIFIER_COEFFICIENT_DURABILITY)

        hp = hero_feature.hp.split('|')
        hp[1] = self.__plus_features(hp[1],
                int(hero_feature.health) * settings.MODIFIER_COEFFICIENT_HP)
        if not self.hero.id:
            hp[0] = hp[1]
        hero_feature.hp = '|'.join(hp)

        capacity = hero_feature.capacity.split('|')
        capacity[1] = self.__plus_features(capacity[1],
                                           int(hero_feature.strength) *
                                        settings.MODIFIER_COEFFICIENT_CAPACITY)
        hero_feature.capacity = '|'.join(capacity)

    def __featureskill_help(self, skill, feature, plus):
        hero_feature = self.hero.feature
        heroskill_level = self.hero.heroheroskill_set.get(skill=skill).level
        
        if feature == Hero.FEATURE_STRENGTH:
            hero_feature.strength = \
                                self.__plus_features(hero_feature.strength,
                                                     plus * heroskill_level)
        elif feature == Hero.FEATURE_DEXTERITY:
            hero_feature.dexterity = \
                                self.__plus_features(hero_feature.dexterity,
                                                     plus * heroskill_level)
        elif feature == Hero.FEATURE_INTUITION:
            hero_feature.intuition = \
                                self.__plus_features(hero_feature.intuition,
                                                     plus * heroskill_level)
        elif feature == Hero.FEATURE_HEALTH:
            hero_feature.health = self.__plus_features(hero_feature.health,
                                                       plus * heroskill_level)

        elif feature == Hero.FEATURE_SWORDS:
            hero_feature.swords = self.__plus_features(hero_feature.swords,
                                                       plus * heroskill_level)
        elif feature == Hero.FEATURE_AXES:
            hero_feature.axes = self.__plus_features(hero_feature.axes,
                                                     plus * heroskill_level)
        elif feature == Hero.FEATURE_KNIVES:
            hero_feature.knives = self.__plus_features(hero_feature.knives,
                                                       plus * heroskill_level)
        elif feature == Hero.FEATURE_CLUBS:
            hero_feature.clubs = self.__plus_features(hero_feature.clubs,
                                                      plus * heroskill_level)
        elif feature == Hero.FEATURE_SHIELDS:
            hero_feature.shields = self.__plus_features(hero_feature.shields,
                                                        plus * heroskill_level)

        elif feature == Hero.FEATURE_PROTECTION_HEAD:
            hero_feature.protection_head = str(plus * heroskill_level)
        elif feature == Hero.FEATURE_PROTECTION_BREAST:
            hero_feature.protection_breast = str(plus * heroskill_level)
        elif feature == Hero.FEATURE_PROTECTION_ZONE:
            hero_feature.protection_zone = str(plus * heroskill_level)
        elif feature == Hero.FEATURE_PROTECTION_LEGS:
            hero_feature.protection_legs = str(plus * heroskill_level)

        elif feature == Hero.FEATURE_DAMAGE_MIN:
            hero_feature.damage_min = str(plus * heroskill_level)
        elif feature == Hero.FEATURE_DAMAGE_MAX:
            hero_feature.damage_max = str(plus * heroskill_level)
            
        elif feature == Hero.FEATURE_ACCURACY:
            hero_feature.accuracy = str(plus * heroskill_level)
        elif feature == Hero.FEATURE_DODGE:
            hero_feature.dodge = str(plus * heroskill_level)
        elif feature == Hero.FEATURE_DEVASTATE:
            hero_feature.devastate = str(plus * heroskill_level)
        elif feature == Hero.FEATURE_DURABILITY:
            hero_feature.durability = str(plus * heroskill_level)

        elif feature == Hero.FEATURE_BLOCK_BREAK:
            hero_feature.block_break = str(plus * heroskill_level)
        elif feature == Hero.FEATURE_ARMOR_BREAK:
            hero_feature.armor_break = str(plus * heroskill_level)

        elif feature == Hero.FEATURE_HP:
            hp = hero_feature.hp.split('|')
            hp[1] = self.__plus_features(hp[1], plus * heroskill_level)
            hero_feature.hp = '|'.join(hp)

        elif feature == Hero.FEATURE_CAPACITY:
            capacity = hero_feature.capacity.split('|')
            capacity[1] = self.__plus_features(capacity[1],
                                               plus * heroskill_level)
            hero_feature.capacity = '|'.join(capacity)

    def __featurething_help(self, thing):
        hero_feature = self.hero.feature
        
        hero_feature.strength = self.__plus_features(hero_feature.strength,
                                                     thing.strength_give)
        hero_feature.dexterity = self.__plus_features(hero_feature.dexterity,
                                                      thing.dexterity_give)
        hero_feature.intuition = self.__plus_features(hero_feature.intuition,
                                                      thing.intuition_give)
        hero_feature.health = self.__plus_features(hero_feature.health,
                                                   thing.health_give)

        hero_feature.swords = self.__plus_features(hero_feature.swords,
                                                   thing.swords_give)
        hero_feature.axes = self.__plus_features(hero_feature.axes,
                                                 thing.axes_give)
        hero_feature.knives = self.__plus_features(hero_feature.knives,
                                                   thing.knives_give)
        hero_feature.clubs = self.__plus_features(hero_feature.clubs,
                                                  thing.clubs_give)
        hero_feature.shields = self.__plus_features(hero_feature.shields,
                                                    thing.shields_give)

        hero_feature.damage_min = self.__plus_features(hero_feature.damage_min,
                                                       thing.damage_min)
        hero_feature.damage_max = self.__plus_features(hero_feature.damage_max,
                                                       thing.damage_max)

        hero_feature.protection_head = self.__plus_features(
                                                hero_feature.protection_head,
                                                        thing.protection_head)
        hero_feature.protection_breast = self.__plus_features(
                                                hero_feature.protection_breast,
                                                    thing.protection_breast)
        hero_feature.protection_zone = self.__plus_features(
                                                hero_feature.protection_zone,
                                                        thing.protection_zone)
        hero_feature.protection_legs = self.__plus_features(
                                                hero_feature.protection_legs,
                                                        thing.protection_legs)

        hero_feature.accuracy = self.__plus_features(hero_feature.accuracy,
                                                     thing.accuracy)
        hero_feature.dodge = self.__plus_features(hero_feature.dodge,
                                                  thing.dodge)
        hero_feature.devastate = self.__plus_features(hero_feature.devastate,
                                                      thing.devastate)
        hero_feature.durability = self.__plus_features(hero_feature.durability,
                                                       thing.durability)
        hero_feature.block_break = \
                                self.__plus_features(hero_feature.block_break,
                                                     thing.block_break)
        hero_feature.armor_break = \
                                self.__plus_features(hero_feature.armor_break,
                                                     thing.armor_break)

        if thing.hp:
            hp = hero_feature.hp.split('|')
            hp[1] = self.__plus_features(hp[1], thing.hp)
            hero_feature.hp = '|'.join(hp)

        hero_feature.strike_count = \
                                self.__plus_features(hero_feature.strike_count,
                                                     thing.strike_count)
        hero_feature.block_count = \
                                self.__plus_features(hero_feature.block_count,
                                                     thing.block_count)

        if thing.capacity:
            capacity = hero_feature.capacity.split('|')
            capacity[1] = self.__plus_features(capacity[1], thing.capacity)
            hero_feature.capacity = '|'.join(capacity)

        if thing.type == Thing.TYPE_SHIELD:
            hero_feature.block_count = \
                            self.__plus_features(hero_feature.block_count, 1)

    def __featureherothing_help(self, feature, plus):
        hero_feature = self.hero.feature
        
        if feature == Hero.FEATURE_STRENGTH:
            hero_feature.strength = self.__plus_features(hero_feature.strength,
                                                         plus)
        elif feature == Hero.FEATURE_DEXTERITY:
            hero_feature.dexterity = \
                            self.__plus_features(hero_feature.dexterity, plus)
        elif feature == Hero.FEATURE_INTUITION:
            hero_feature.intuition = \
                            self.__plus_features(hero_feature.intuition, plus)
        elif feature == Hero.FEATURE_HEALTH:
            hero_feature.health = \
                                self.__plus_features(hero_feature.health, plus)

        elif feature == Hero.FEATURE_SWORDS:
            hero_feature.swords = self.__plus_features(hero_feature.swords,
                                                       plus)
        elif feature == Hero.FEATURE_AXES:
            hero_feature.axes = self.__plus_features(hero_feature.axes, plus)
        elif feature == Hero.FEATURE_KNIVES:
            hero_feature.knives = self.__plus_features(hero_feature.knives,
                                                       plus)
        elif feature == Hero.FEATURE_CLUBS:
            hero_feature.clubs = self.__plus_features(hero_feature.clubs, plus)
        elif feature == Hero.FEATURE_SHIELDS:
            hero_feature.shields = self.__plus_features(hero_feature.shields,
                                                        plus)

        elif feature == Hero.FEATURE_PROTECTION_HEAD:
            hero_feature.protection_head = \
                            self.__plus_features(hero_feature.protection_head,
                                                 plus)
        elif feature == Hero.FEATURE_PROTECTION_BREAST:
            hero_feature.protection_breast = \
                        self.__plus_features(hero_feature.protection_breast,
                                             plus)
        elif feature == Hero.FEATURE_PROTECTION_ZONE:
            hero_feature.protection_zone = \
                            self.__plus_features(hero_feature.protection_zone,
                                                 plus)
        elif feature == Hero.FEATURE_PROTECTION_LEGS:
            hero_feature.protection_legs = \
                            self.__plus_features(hero_feature.protection_legs,
                                                 plus)

        elif feature == Hero.FEATURE_DAMAGE_MIN:
            hero_feature.damage_min = \
                            self.__plus_features(hero_feature.damage_min, plus)
        elif feature == Hero.FEATURE_DAMAGE_MAX:
            hero_feature.damage_max = \
                            self.__plus_features(hero_feature.damage_max, plus)

        elif feature == Hero.FEATURE_ACCURACY:
            hero_feature.accuracy = self.__plus_features(hero_feature.accuracy,
                                                         plus)
        elif feature == Hero.FEATURE_DODGE:
            hero_feature.dodge = self.__plus_features(hero_feature.dodge, plus)
        elif feature == Hero.FEATURE_DEVASTATE:
            hero_feature.devastate = \
                            self.__plus_features(hero_feature.devastate, plus)
        elif feature == Hero.FEATURE_DURABILITY:
            hero_feature.durability = \
                            self.__plus_features(hero_feature.durability, plus)

        elif feature == Hero.FEATURE_BLOCK_BREAK:
            hero_feature.block_break = \
                        self.__plus_features(hero_feature.block_break, plus)
        elif feature == Hero.FEATURE_ARMOR_BREAK:
            hero_feature.armor_break = \
                        self.__plus_features(hero_feature.armor_break, plus)

        elif feature == Hero.FEATURE_HP:
            hp = hero_feature.hp.split('|')
            hp[1] = self.__plus_features(hp[1], plus)
            hero_feature.hp = '|'.join(hp)

        elif feature == Hero.FEATURE_CAPACITY:
            capacity = hero_feature.capacity.split('|')
            capacity[1] = self.__plus_features(capacity[1], plus)
            hero_feature.capacity = '|'.join(capacity)

        elif feature == Hero.FEATURE_STRIKE_COUNT:
            hero_feature.strike_count = \
                        self.__plus_features(hero_feature.strike_count, plus)
        elif feature == Hero.FEATURE_BLOCK_COUNT:
            hero_feature.block_count = \
                        self.__plus_features(hero_feature.block_count, plus)

    def __plus_features(self, hero_feature, other_feature):
        if other_feature:
            return str(int(hero_feature) + int(round(other_feature)))
        return hero_feature

    def level_up(self):
        if self.hero.id:
            try:
                tableexperience = TableExperience.objects. \
                                        filter(level__gt=self.hero.level). \
                            exclude(experience__gte=self.hero.experience). \
                                                        order_by('level')[0]

                self.hero.number_of_abilities += \
                                            tableexperience.number_of_abilities
                self.hero.number_of_skills += tableexperience.number_of_skills
                self.hero.number_of_parameters += \
                                        tableexperience.number_of_parameters
                self.hero.money += tableexperience.money
                self.hero.level += 1
                
                self.hero.save()
            except IndexError:
                pass

        else:
            try:
                tableexperience = TableExperience.objects.get(experience=0)

                self.hero.number_of_abilities += \
                                            tableexperience.number_of_abilities
                self.hero.number_of_skills += tableexperience.number_of_skills
                self.hero.number_of_parameters += \
                                        tableexperience.number_of_parameters
                self.hero.money += tableexperience.money
            except TableExperience.DoesNotExist:
                pass

    def update_capacity(self):
        all_weight = 0
        for herothing in self.hero.herothing_set.filter(away=False):
            all_weight += herothing.thing.weight

        hero_capacity = self.hero.feature.capacity.split('|')
        hero_capacity[0] = str(all_weight)
        self.hero.feature.capacity = '|'.join(hero_capacity)
        self.hero.feature.save()

    def get_island(self):
         return Island.objects. \
                    get(slug=self.hero.location.split('&')[0].split(':')[0])

    def get_position_on_island(self):
        return [ int(i) for i in
                    self.hero.location.split('&')[0].split(':')[1].split('|') ]

    def update_position_on_island(self, coordinate_x, coordinate_y):
        self.hero.location = '%s:%s|%s|%s' % (self.hero.location.split('_')[0],
                                              coordinate_x, coordinate_y,
                                              int(time.time()))
        self.hero.save()

    def get_location(self):
        location = self.hero.location.split('&')

        island_location = location[0].split('|')
        del island_location[2]
        location[0] = '|'.join(island_location)

        return '&'.join(location)

    def get_combat(self, is_active=None):
        try:
            combat = Combat.objects.filter(combatwarrior__hero=self.hero,
                                           combatwarrior__is_quit=False).get()
            if is_active == None:
                return combat
            elif combat.is_active == is_active:
                return combat
            else:
                return None
        except Combat.DoesNotExist:
            return None

    def set_hp(self, hp=-1):
        if hp == -1:
            hp = self.hero.feature.hp.split('|')[0]
        self.hero.feature.hp = '%s|%s|%s' % (hp,
                                            self.hero.feature.hp.split('|')[1],
                                             time.time())
        self.hero.feature.save()

    def update_hp(self):

        hp = self.hero.feature.hp.split('|')
        current_time = float(hp[2])
        max_hp = int(hp[1])

        if max_hp == int(float(hp[0])):
            return

        one_hp_sec = settings.HP_REGENERATION_DELAY / max_hp
        current_hp = float(hp[0]) + (time.time() - current_time) / one_hp_sec

        if current_hp > max_hp:
            current_hp = max_hp

        self.hero.feature.hp = '%s|%s|%s' % (current_hp, max_hp, time.time())
        self.hero.feature.save()

from django.db.models import Q
from django.conf import settings

from combat.models import Combat, CombatWarrior, CombatLog
from hero.models import Hero
from tableexperience.models import TableExperience
from bot.models import Bot

from hero.manipulation import HeroM
from bot.manipulation import BotM

import time
import random
import datetime

class CombatM:
    def __init__(self, combat, hero):
        self.combat = combat
        self.hero = hero

    # Before combat
    def is_cancel(self):
        if self.combat.combatwarrior_set.count() == 1:
            return True
        else:
            return False

    # For duel
    def is_fight(self):
        if self.combat.type == Combat.TYPE_DUEL and \
                                            self.combat.combatwarrior_set. \
                                get(hero=self.hero).team == Combat.TEAM_FIRST:
            return self.combat.combatwarrior_set.count() == 2
        else:
            return False

    def is_refuse(self):
        if self.combat.type == Combat.TYPE_DUEL:
            return self.combat.combatwarrior_set.count() == 2
        else:
            return False
    # End for duel

    # Combat update
    def update_combats(self, type):
        combats = Combat.objects.filter(type=type,
                                        is_active=Combat.IS_ACTIVE_WAIT)

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
                self.__start_combat(combat, type)
                continue

            time_start = int(time.mktime(combat.start_date_time.timetuple()))
            if (int(time.time()) - time_start) >= combat.time_wait:
                if (one_team_count > 0 and two_team_count > 0 and
                    type == Combat.TYPE_GROUP) or \
                    (one_team_count > 0 and type == Combat.TYPE_CHAOTIC):
                    self.__start_combat(combat, type)
                else:
                    if combat == self.combat:
                        self.combat = None
                    combat.delete()
            else:
                combat.time_wait_left = combat.time_wait - (int(time.time()) -
                                                                    time_start)
                combat.save()

    def __start_combat(self, combat, type):
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
                                                    id=combatwarriors[i].id)
                combatwarrior.team = Combat.TEAM_SECOND
                combatwarrior.save()

        if combat == self.combat:
            self.combat.is_active = Combat.IS_ACTIVE_FIGHT
        combat.is_active = Combat.IS_ACTIVE_FIGHT
        combat.save()
    # End combat update

    def is_active(self):
        if self.combat.is_active == Combat.IS_ACTIVE_FIGHT or \
           self.combat.is_active == Combat.IS_ACTIVE_AFTER_FIGHT:
            return True

        return False
    # End before combat

    # Combat inside
    def get_enemies(self, team):
        if team == Combat.TEAM_FIRST:
            heroes = [ i.hero for i in self.combat.combatwarrior_set.
                                    filter(is_dead=False).exclude(team=team)
                        if not self.combat.combatlog_set.filter(
                                                            hero_one=self.hero,
                                                            hero_two=i.hero,
                                                                is_past=False,
                                                    warrior_two_wstrike=None)
                                                                and i.hero ]
        else:
            heroes = [ i.hero for i in self.combat.combatwarrior_set. \
                                    filter(is_dead=False).exclude(team=team)
                        if not self.combat.combatlog_set.filter(
                                                            hero_two=self.hero,
                                                            hero_one=i.hero,
                                                                is_past=False,
                                                    warrior_one_wstrike=None)
                                                                and i.hero ]


        bots = [ i.bot for i in self.combat.combatwarrior_set. \
                                    filter(is_dead=False).exclude(team=team)
                                                                    if i.bot ]

        return heroes + bots

    def get_enemy(self, enemies, cur_enemy_id_fn):
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

    def is_dead(self, hero, bot=None):
        return self.combat.combatwarrior_set.filter(hero=hero, bot=bot,
                                                    is_dead=True).exists()

    def is_draw(self):
        return self.combat.combatwarrior_set.all().count() == \
                    self.combat.combatwarrior_set.filter(is_dead=True).count()

    def is_win(self, team, is_draw):
        return not self.combat.combatwarrior_set.filter(is_dead=False). \
                                    exclude(team=team).exists() and not is_draw

    def is_lose(self, team, is_draw):
        return not self.combat.combatwarrior_set.filter(is_dead=False,
                                                        team=team). \
                                                    exists() and not is_draw

    def is_timeout(self, team, is_bot_call=False):

        count_in_team = self.combat.combatwarrior_set.filter(team=team,
                                                             bot=None,
                                                             is_dead=False). \
                                                                        count()
        if count_in_team and is_bot_call:
            return False

        count_in_not_answer_team = self.combat.combatwarrior_set. \
                                                    filter(is_dead=False). \
                                                    exclude(team=team).count()
        datetime_limit = datetime.datetime.fromtimestamp(time.time() - \
                                                         self.combat.time_out)

        if team == Combat.TEAM_FIRST:
            count_not_answer = self.combat.combatlog_set.filter(
                                                    warrior_two_wstrike=None,
                                                                is_past=False,
                                            time__lte=datetime_limit).count()
        else:
            count_not_answer = self.combat.combatlog_set.filter(
                                                    warrior_one_wstrike=None,
                                                                is_past=False,
                                            time__lte=datetime_limit).count()

        was_actions = self.combat.combatlog_set. \
                                        filter((~Q(warrior_one_wstrike=None) &
                                                ~Q(warrior_two_wstrike=None)) |
                                               Q(is_start=True),
                                               time__gte=datetime_limit). \
                                                                    exists()

        all_worriors_not_answer = \
        ((count_in_team * count_in_not_answer_team) - count_not_answer) == 0
        return (all_worriors_not_answer and not was_actions)

    def is_warrior_in_combat(self, hero, bot):
        return self.combat.objects.filter(Q(combatwarrior__hero=hero) |
                                          Q(combatwarrior__bot=bot),
                                          combatwarrior__is_dead=False,
                                          combatwarrior__is_out=False).exists()

    def is_anybody_not_quit(self):
        return self.combat.combatwarrior_set.filter(is_quit=False).exists()

    def write_log_message(self, is_start=False, is_finish=False, win_team=None,
                          is_dead=False, is_join=False, hero=None, bot=None):
        if is_start:
            if self.combat.combatlog_set.filter(is_start=True).exists():
                return

            warriors_one = []
            warriors_two = []
            for combatwarrior in self.combat.combatwarrior_set.all():
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

            self.combat.combatlog_set.create(is_start=True,
                                             text='[warriors_one]' +
                                                  ','.join(warriors_one) +
                                                  '[/warriors_one]' +
                                                  '[warriors_two]' +
                                                  ','.join(warriors_two) +
                                                  '[/warriors_two]')

        if is_finish:
            if self.combat.combatlog_set.filter(is_finish=True).exists():
                return

            if win_team == None:
                warriors_one = []
                warriors_two = []
                for combatwarrior in self.combat.combatwarrior_set.all():
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

                self.combat.combatlog_set.create(is_finish=True,
                                                 text='[warriors_one]' +
                                                      ','.join(warriors_one) +
                                                      '[/warriors_one]' +
                                                      '[warriors_two]' +
                                                      ','.join(warriors_two) +
                                                      '[/warriors_two]')

            else:
                warriors = []
                for combatwarrior in self.combat.combatwarrior_set. \
                                                        filter(team=win_team):
                    if combatwarrior.hero:
                        warriors.append(str(combatwarrior.hero))
                    else:
                        warriors.append(str(combatwarrior.bot))

                self.combat.combatlog_set.create(is_finish=True,
                                                 text='[warriors_one]' +
                                                      ','.join(warriors) +
                                                      '[/warriors_one]')

        if is_dead:
            warrior = hero if hero else bot
            self.combat.combatlog_set.create(is_dead=True, hero_one=hero,
                                             bot_one=bot, text='[warrior]' +
                                                               str(warrior) +
                                                               '[/warrior]')
        if is_join:
            self.combat.combatlog_set.create(is_join=True, hero_one=hero,
                                             text='[warrior]' + str(hero) +
                                                  '[/warrior]')

    def write_log_strikes(self, team, hero_two, bot, strikes, blocks):

        combatlog = self.__get_log(team, hero_two, bot)

        if combatlog is None:
            strikes_s = '|'.join(strikes)
            blocks_s = '|'.join(blocks)

            if team == Combat.TEAM_FIRST:
                tcombatlog = self.combat.combatlog_set.create(
                                                            hero_one=self.hero,
                                                            hero_two=hero_two,
                                                              bot_two=bot,
                                                              is_past=False,
                                                warrior_one_wstrike=strikes_s,
                                                warrior_one_wblock=blocks_s)
            else:
                tcombatlog = self.combat.combatlog_set.create(
                                                            hero_one=hero_two,
                                                              bot_one=bot,
                                                            hero_two=self.hero,
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

            warrior = self.hero

            accuracy_p = settings.COMBAT_RANGE_ACCURACY
            devastate_p = settings.COMBAT_RANGE_DEVASTATE
            block_break_p = settings.COMBAT_RANGE_BLOCK_BREAK
            armor_break_p = settings.COMBAT_RANGE_ARMOR_BREAK
            damage_p = settings.COMBAT_RANGE_DAMAGE

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
                    accuracy = devastate = block = block_break = \
                    armor_break = is_block = False

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
                                    combatwarrior = self.combat. \
                                        combatwarrior_set.get(hero=warrior_two)
                                else:
                                    combatwarrior = self.combat. \
                                        combatwarrior_set.get(bot=warrior_two)
                                combatwarrior.is_dead = True
                                combatwarrior.save()
                                dead_warriors.append({'warrior': warrior_two,
                                                'team': combatwarrior.team})

                            if type(warrior_two) == Hero:
                                HeroM(warrior_two).set_hp(current_hp)
                            else:
                                warrior_two.feature.hp = '%s|%s' % (current_hp,
                                        warrior_two.feature.hp.split('|')[1])
                                warrior_two.feature.save()

                    strikes[i] = str(strike) + '_' + str(strike_damage) + \
                                 '_' + str(int(block)) + '_' + \
                                 str(int(block_break)) + '_' + \
                                 str(int(not accuracy)) + '_' + \
                                 str(int(devastate)) + '_' + \
                                 str(int(armor_break))

                    damage_bamp += strike_damage
                    combatlog.text += '[warrior_one]' + str(warrior) + \
                                      '[/warrior_one][warrior_two]' + \
                                      str(warrior_two) + \
                                      '[/warrior_two][strikes]' + \
                                      strikes[i] + '[/strikes][blocks]' + \
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

            self.after_death(dead_warriors)

    def __get_log(self, team, hero_two, bot):
        try:
            if team == Combat.TEAM_FIRST:
                return self.combat.combatlog_set.filter(hero_one=self.hero,
                                                        hero_two=hero_two,
                                                        bot_two=bot,
                                                        is_past=False).get()
            else:
                return self.combat.combatlog_set.filter(hero_two=self.hero,
                                                        hero_one=hero_two,
                                                        bot_one=bot,
                                                        is_past=False).get()
        except CombatLog.DoesNotExist:
            return None

    def after_death(self, dead_warriors):
        for dead_warrior in dead_warriors:
            if dead_warrior['team'] == Combat.TEAM_FIRST:
                self.combat.combatlog_set.filter(is_past=False,
                                            hero_one=dead_warrior['warrior'],
                                            bot_one=dead_warrior['warrior']). \
                                                                    delete()
            else:
                self.combat.combatlog_set.filter(is_past=False,
                                            hero_two=dead_warrior['warrior'],
                                            bot_two=dead_warrior['warrior']). \
                                                                    delete()
            is_warrior_hero = type(dead_warrior['warrior']) == Hero
            self.write_log_message(is_dead=True,
                    hero=dead_warrior['warrior'] if is_warrior_hero else None,
                bot=dead_warrior['warrior'] if not is_warrior_hero else None)
    # End combat inside

    # Bots
    def update_bots_timeout(self):
        try:
            combatwarrior = self.combat.combatwarrior_set. \
                            filter(is_dead=False).exclude(bot=None)[0:1].get()
            team = combatwarrior.team
            if self.is_timeout(team, True):
                dead_warriors = []
                for combatwarrior in self.combat.combatwarrior_set. \
                                    filter(is_dead=False).exclude(team=team):
                    HeroM(combatwarrior.hero).set_hp(0)
                    combatwarrior.is_dead = True
                    combatwarrior.save()
                    dead_warriors.append({'warrior': combatwarrior.hero,
                                          'team': combatwarrior.team})

                self.after_death(dead_warriors)
                return True
        except CombatWarrior.DoesNotExist:
            return False

    def free_bots(self):
        for combatwarrior in self.combat.combatwarrior_set.exclude(bot=None):
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
            BotM(combatwarrior.bot).restore_hp()

    def update_bots_in_combats(self, coordinate_x, coordinate_y):
        bots = Bot.objects.filter(coordinate_x1__lte=coordinate_x,
                                  coordinate_y1__lte=coordinate_y,
                                  coordinate_x2__gte=coordinate_x,
                                  coordinate_y2__gte=coordinate_y,
                                  in_combat=True)

        for bot in bots:
            self.combat = Combat.objects.filter(combatwarrior__bot=bot,
                                           combatwarrior__is_dead=False,
                                           is_active=Combat.IS_ACTIVE_FIGHT). \
                                                                        get()

            team = self.combat.combatwarrior_set.get(bot=bot).team

            if self.is_timeout(team, True):
                dead_warriors = []
                for combatwarrior in self.combat.combatwarrior_set. \
                                    filter(is_dead=False).exclude(team=team):
                    HeroM(combatwarrior.hero).set_hp(0)
                    combatwarrior.is_dead = True
                    combatwarrior.save()
                    dead_warriors.append({'warrior': combatwarrior.hero,
                                          'team': combatwarrior.team})

                self.after_death(dead_warriors)
                self.free_bots()
# End bots
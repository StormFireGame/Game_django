from django.db import models

from hero.models import Hero
from bot.models import Bot

##
class Combat(models.Model):
#
    STRIKES = ((0, 'Head'), (1, 'Breast'), (2, 'Zone'), (3, 'Legs'))
    BLOCKS = ((0, 'Head'), (1, 'Breast'), (2, 'Zone'), (3, 'Legs'))

    TEAM_FIRST = 0
    TEAM_SECOND = 1
#
    TEAMS = ((TEAM_FIRST, 'First'), (TEAM_SECOND, 'Second'))

    TYPE_DUEL = 0
    TYPE_GROUP = 1
    TYPE_CHAOTIC = 2
    TYPE_TERRITORIAL = 3
#
    TYPES = ((TYPE_DUEL, 'Duel'), (TYPE_GROUP, 'Group'), 
             (TYPE_CHAOTIC, 'Chaotic'), (TYPE_TERRITORIAL, 'Territorial'))
    type = models.SmallIntegerField(default=0, choices=TYPES)

    IS_ACTIVE_WAIT = 0
    IS_ACTIVE_FIGHT = 1
    IS_ACTIVE_AFTER_FIGHT = 2
    IS_ACTIVE_PAST = 3
#
    IS_ACTIVES = ((IS_ACTIVE_WAIT, 'Wait'), (IS_ACTIVE_FIGHT, 'Fight'), 
                  (IS_ACTIVE_AFTER_FIGHT, 'After fight'), 
                  (IS_ACTIVE_PAST, 'Past'),)
    is_active = models.SmallIntegerField(default=0, choices=IS_ACTIVES)
    time_out = models.IntegerField(default=60)
#
    INJURIES = ((0, 'Low'), (1, 'Middle'), (2, 'Top'))
    injury = models.SmallIntegerField(default=0, choices=INJURIES)
    with_things = models.BooleanField(default=True, blank=True)
    time_wait = models.IntegerField(default=360, null=True, blank=True)
    time_wait_left = models.IntegerField(default=360, null=True, blank=True)
    one_team_count = models.IntegerField(null=True, blank=True, default=99)
    two_team_count = models.IntegerField(null=True, blank=True, default=99)
    one_team_lvl_min = models.IntegerField(null=True, blank=True, default=0)
    one_team_lvl_max = models.IntegerField(null=True, blank=True, default=99)
    two_team_lvl_min = models.IntegerField(null=True, blank=True,default=0)
    two_team_lvl_max = models.IntegerField(null=True, blank=True, default=99)
    location = models.CharField(max_length=32)
    start_date_time = models.DateTimeField(auto_now_add=True)
    end_date_time = models.DateTimeField(null=True, blank=True)
    win_team = models.SmallIntegerField(null=True, blank=True, default=-1)
    
    class Meta:
        db_table = 'Combat'
        ordering = ['-start_date_time']
    
    def __unicode__(self):
        return '%s %s' % (self.TYPES[self.type][1], 
                          self.IS_ACTIVES[self.is_active][1])

class CombatWarrior(models.Model):
    combat = models.ForeignKey(Combat)
    hero = models.ForeignKey(Hero, null=True, blank=True)
    bot = models.ForeignKey(Bot, null=True, blank=True)
    
    team = models.SmallIntegerField(default=0, choices=Combat.TEAMS)
    is_dead = models.BooleanField(default=False)
    is_join = models.BooleanField(default=False)
    is_out = models.BooleanField(default=False)
    is_quit = models.BooleanField(default=False)

    class Meta:
        db_table = 'CombatWarrior'
    
    def __unicode__(self):
        if self.hero:
            return str(self.hero)
        else:
            return str(self.bot)

class CombatLog(models.Model):
    combat = models.ForeignKey(Combat)
    
    hero_one = models.ForeignKey(Hero, null=True, related_name='hero_one', 
                                 blank=True)
    hero_two = models.ForeignKey(Hero, null=True, related_name='hero_two', 
                                 blank=True)
    bot_one = models.ForeignKey(Bot, null=True, related_name='bot_one', 
                                blank=True)
    bot_two = models.ForeignKey(Bot, null=True, related_name='bot_two', 
                                blank=True)
    
    warrior_one_wstrike = models.CharField(max_length=32, null=True, 
                                           blank=True)
    warrior_two_wstrike = models.CharField(max_length=32, null=True, 
                                           blank=True)
    warrior_one_wblock = models.CharField(max_length=32, null=True, blank=True)
    warrior_two_wblock = models.CharField(max_length=32, null=True, blank=True)
    
    warrior_one_damage = models.IntegerField(null=True, blank=True)
    warrior_two_damage = models.IntegerField(null=True, blank=True)
    warrior_one_experience = models.IntegerField(null=True, blank=True)
    warrior_two_experience = models.IntegerField(null=True, blank=True)
    
    is_join = models.BooleanField(default=False)
    is_out = models.BooleanField(default=False)
    is_start = models.BooleanField(default=False)
    is_finish = models.BooleanField(default=False)
    is_dead = models.BooleanField(default=False)
    hp_plus = models.IntegerField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    time = models.DateTimeField(auto_now=True)
    
    is_past = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'CombatLog'
        ordering = ['-time']
    
    def __unicode__(self):
        return self.text if self.text else ''
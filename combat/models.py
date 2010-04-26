from django.db import models

from hero.models import Hero
from bot.models import Bot

class Combat(models.Model):
#
    TYPES = ((0, 'Duel'), (1, 'Group'), (2, 'Chaotic'), (3, 'Territorial'))
    type = models.SmallIntegerField(default=0, choices=TYPES)
#
    IS_ACTIVES = ((0, 'Wait'), (1, 'Fight'), (2, 'Closed'),)
    is_active = models.SmallIntegerField(default=0, choices=IS_ACTIVES)
    time_out = models.IntegerField(default=60)
#
    INJURIES = ((0, 'Low'), (1, 'Middle'), (2, 'Top'))
    injury = models.SmallIntegerField(default=0, choices=INJURIES)
    with_things = models.BooleanField(default=True, blank=True)
    time_wait = models.IntegerField(default=180, null=True, blank=True)
    one_team_count = models.IntegerField(null=True, blank=True)
    two_team_count = models.IntegerField(null=True, blank=True)
    one_team_lvl_min = models.IntegerField(null=True, blank=True)
    one_team_lvl_max = models.IntegerField(null=True, blank=True)
    two_team_lvl_min = models.IntegerField(null=True, blank=True)
    two_team_lvl_max = models.IntegerField(null=True, blank=True)
    location = models.CharField(max_length=32, blank=True)
    start_date_time = models.DateTimeField(auto_now_add=True)
    end_date_time = models.DateTimeField(null=True, blank=True)
        
    class Meta:
        db_table = 'Combat'

class CombatHero(models.Model):
    combat = models.ForeignKey(Combat)
    hero = models.ForeignKey(Hero, null=True, blank=True)
    bot = models.ForeignKey(Bot, null=True, blank=True)
#
    TEAMS = ((0, 'First'), (1, 'Second'))
    team = models.SmallIntegerField(default=0, choices=TEAMS)
    is_dead = models.BooleanField(default=False)
    is_join = models.BooleanField(default=False)
    is_out = models.BooleanField(default=False)

    class Meta:
        db_table = 'CombatHero'
    
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
    
    hero_one_wstrike = models.CharField(max_length=32, null=True, blank=True)
    hero_two_wstrike = models.CharField(max_length=32, null=True, blank=True)
    hero_one_wblock = models.CharField(max_length=32, null=True, blank=True)
    hero_two_wblock = models.CharField(max_length=32, null=True, blank=True)
    
    hero_join = models.BooleanField(default=False)
    hero_out = models.BooleanField(default=False)
    hp_plus = models.IntegerField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    time = models.TimeField(auto_now=True)
    
    class Meta:
        db_table = 'CombatLog'
    
    def __unicode__(self):
        if self.hero_one:
            h = self.hero_one
        elif self.hero_two:
            h = self.hero_two
        elif self.bot_one:
            h = self.bot_one
        else:
            h = self.bot_two
        
        h1 = ''   
        if self.bot_two:
            h1 = self.bot_two
        elif self.bot_one:
            h1 = self.bot_one
        elif self.hero_two:
            h1 = self.hero_two

        return '%s vs %s' % (h, h1)
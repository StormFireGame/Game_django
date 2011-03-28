from django.db import models
from django.conf import settings

from thing.models import Thing
from island.models import Island

import hashlib

class HeroImage(models.Model):
    image = models.ImageField(upload_to='upload/heroimages')
    is_art = models.BooleanField(default=False)
#    
    SEXS = ((0, 'Male'), (1, 'Female'))
    sex = models.SmallIntegerField(default=0, choices=SEXS)
    
    class Meta:
        db_table = 'HeroImage'
        
    def __unicode__(self):
        return str(self.image).split('/')[-1]
        
    def thumbnail(self):
        url = '%s%s' % (settings.MEDIA_URL, self.image)
        return '<img src="%s" width="%s" height="%s" />' % (url, '', '')
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True

class HeroSkill(models.Model):
    name = models.CharField(max_length=32, unique=True)
    
    class Meta:
        db_table = 'HeroSkill'
        
    def __unicode__(self):
        return self.name

class HeroFeature(models.Model):
    strength = models.CharField(max_length=32, null=True)
    dexterity = models.CharField(max_length=32, null=True)
    intuition = models.CharField(max_length=32, null=True)
    health = models.CharField(max_length=32, null=True)
    
    swords = models.CharField(max_length=32, null=True)
    axes = models.CharField(max_length=32, null=True)
    knives = models.CharField(max_length=32, null=True)
    clubs = models.CharField(max_length=32, null=True)
    shields = models.CharField(max_length=32, null=True)
    
    protection_head = models.CharField(max_length=32, null=True, default=0)
    protection_breast = models.CharField(max_length=32, null=True, default=0)
    protection_zone = models.CharField(max_length=32, null=True, default=0)
    protection_legs = models.CharField(max_length=32, null=True, default=0)
    
    damage_min = models.CharField(max_length=32, null=True)
    damage_max = models.CharField(max_length=32, null=True)
    
    accuracy = models.CharField(max_length=32, null=True)
    dodge = models.CharField(max_length=32, null=True)
    devastate = models.CharField(max_length=32, null=True)
    durability = models.CharField(max_length=32, null=True)
    block_break = models.CharField(max_length=32, null=True, default=0)
    armor_break = models.CharField(max_length=32, null=True, default=0)
    
    hp = models.CharField(max_length=128, null=True)
    
    capacity = models.CharField(max_length=32, null=True)
    
    strike_count = models.CharField(max_length=32, null=True)
    block_count = models.CharField(max_length=32, null=True)

    class Meta:
        db_table = 'HeroFeature'

##                   
class Hero(models.Model):
    
    FEATURE_STRENGTH = 0
    FEATURE_DEXTERITY = 1
    FEATURE_INTUITION = 2
    FEATURE_HEALTH = 3
    FEATURE_SWORDS = 4
    FEATURE_AXES = 5
    FEATURE_KNIVES = 6
    FEATURE_CLUBS = 7
    FEATURE_SHIELDS = 8
    FEATURE_PROTECTION_HEAD = 9
    FEATURE_PROTECTION_BREAST = 10
    FEATURE_PROTECTION_ZONE = 11
    FEATURE_PROTECTION_LEGS = 12
    FEATURE_DAMAGE_MIN = 13
    FEATURE_DAMAGE_MAX = 14
    FEATURE_ACCURACY = 15
    FEATURE_DODGE = 16
    FEATURE_DEVASTATE = 17
    FEATURE_DURABILITY = 18
    FEATURE_BLOCK_BREAK = 19
    FEATURE_ARMOR_BREAK = 20
    FEATURE_HP = 21
    FEATURE_CAPACITY = 22
    FEATURE_STRIKE_COUNT = 23
    FEATURE_BLOCK_COUNT = 24
#
    FEATURES = ((FEATURE_STRENGTH, 'Strength'), 
                (FEATURE_DEXTERITY, 'Dexterity'), 
                (FEATURE_INTUITION, 'Intuition'), 
                (FEATURE_HEALTH, 'Health'), (FEATURE_SWORDS, 'Swords'), 
                (FEATURE_AXES, 'Axes'), (FEATURE_KNIVES, 'Knives'), 
                (FEATURE_CLUBS, 'Clubs'), (FEATURE_SHIELDS, 'Shields'), 
                (FEATURE_PROTECTION_HEAD, 'Protection head'), 
                (FEATURE_PROTECTION_BREAST, 'Protection breast'), 
                (FEATURE_PROTECTION_ZONE, 'Protection zone'), 
                (FEATURE_PROTECTION_LEGS, 'Protection legs'), 
                (FEATURE_DAMAGE_MIN, 'Damage min'), 
                (FEATURE_DAMAGE_MAX, 'Damage max'), 
                (FEATURE_ACCURACY, 'Accuracy'), 
                (FEATURE_DODGE, 'Dodge'), (FEATURE_DEVASTATE, 'Devastate'), 
                (FEATURE_DURABILITY, 'Durability'), 
                (FEATURE_BLOCK_BREAK, 'Block break'), 
                (FEATURE_ARMOR_BREAK, 'Armor break'), (FEATURE_HP, 'Hp'), 
                (FEATURE_CAPACITY, 'Capacity'))
    
    login = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    email = models.EmailField(max_length=64, unique=True)
    experience = models.IntegerField(default=0)
    money = models.FloatField(default=0.00)
    money_art = models.FloatField(default=0.00)
    location = models.CharField(max_length=1024, blank=True)
    level = models.IntegerField(default=0)
    image = models.ForeignKey(HeroImage, null=True, blank=True)
    feature = models.ForeignKey(HeroFeature)
    
    number_of_wins = models.IntegerField(default=0)
    number_of_losses = models.IntegerField(default=0)
    number_of_draws = models.IntegerField(default=0)
    
    hp = models.IntegerField(default=30)
    
    strength = models.IntegerField(default=3)
    dexterity = models.IntegerField(default=3)
    intuition = models.IntegerField(default=3)
    health = models.IntegerField(default=3)
    swords = models.IntegerField(default=0)
    axes = models.IntegerField(default=0)
    knives = models.IntegerField(default=0)
    clubs = models.IntegerField(default=0)
    shields = models.IntegerField(default=0)
    
    date_of_birthday = models.DateField()
#
    SEXS = ((0, 'Male'), (1, 'Female'))
    sex = models.SmallIntegerField(default=0, choices=SEXS)
    country = models.CharField(max_length=32, blank=True)
    city = models.CharField(max_length=32, blank=True)
    name = models.CharField(max_length=64, blank=True)
    about = models.TextField(blank=True)
    
    number_of_abilities = models.PositiveIntegerField(default=0)
    number_of_skills = models.PositiveIntegerField(default=0)
    number_of_parameters = models.PositiveIntegerField(default=0)
    
    skills = models.ManyToManyField(HeroSkill, through='HeroHeroSkill')
    things = models.ManyToManyField(Thing, through='HeroThing')
        
    class Meta:
        db_table = 'Hero'
        verbose_name_plural = 'Heroes'
    
    def __unicode__(self):
        return '%s [%s]' % (self.login, self.level)
    
    def save(self):
        if not self.id:
            self.password = hashlib.sha1(self.password).hexdigest()
            
            herofeature = HeroFeature()
            herofeature.save()
            self.feature = herofeature
            from hero import heromanipulation
            heromanipulation.hero_feature(self)
            heromanipulation.hero_level_up(self)
            
            if not self.image:
                heroimage = HeroImage.objects.filter(sex=self.sex)[0]
                self.image = heroimage
            
            island = Island.objects.all()[0]
            self.location = '%s_20|20:0' % (island.id)
        else:
            if self.password != Hero.objects.get(id=self.id).password:
                self.password = hashlib.sha1(self.password).hexdigest()
        
        super(Hero, self).save()

class SkillFeature(models.Model):
    heroskill = models.ForeignKey(HeroSkill)
    feature = models.IntegerField(default=0, choices=Hero.FEATURES)
    plus = models.IntegerField()
    
    class Meta:
        db_table = 'SkillFeature'
        unique_together = (('heroskill', 'feature'),)
        
    def __unicode__(self):
        return '%s %s' % (Hero.FEATURES[self.feature][1], self.plus)

class HeroHeroSkill(models.Model):
    hero = models.ForeignKey(Hero)
    skill = models.ForeignKey(HeroSkill)
    level = models.IntegerField()
    
    def __unicode__(self):
        return '%s %s' % (self.skill, self.level)
    
    class Meta:
        db_table = 'HeroHeroSkill'
        unique_together = (('hero', 'skill'),)

class HeroThing(models.Model):
    hero = models.ForeignKey(Hero)
    thing = models.ForeignKey(Thing)
    stability_all = models.IntegerField()
    stability_left = models.IntegerField()
    dressed = models.BooleanField(default=False)
    away = models.BooleanField(default=False)
    
    def __unicode__(self):
        return '%s %s' % (self.hero, self.thing)
    
    class Meta:
        db_table = 'HeroThing'

class HeroThingFeature(models.Model):
    herothing = models.ForeignKey(HeroThing)
    feature = models.IntegerField(default=0, choices=Hero.FEATURES)
    plus = models.IntegerField()
    
    def __unicode__(self):
        return self.herothing.hero
    
    def hero(self):
        return self.herothing.hero
    
    def thing(self):
        return self.herothing.thing
    
    class Meta:
        db_table = 'HeroThingFeature'
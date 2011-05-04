from django.db import models
from django.conf import settings

class Thing(models.Model):
    
    TYPE_SWORD = 0
    TYPE_AXE = 1
    TYPE_KNIVE = 2
    TYPE_CLUBS = 3
    TYPE_SHIELD = 4
    TYPE_HELMET = 5
    TYPE_KOLCHUGA = 6
    TYPE_ARMOR = 7
    TYPE_BELT = 8
    TYPE_PANTS = 9
    TYPE_TREETOP = 10
    TYPE_GLOVE = 11
    TYPE_BOOT = 12
    TYPE_RING = 13
    TYPE_AMULET = 14
    TYPE_POTION = 15
    TYPE_ELIXIR = 16
#
    TYPES = ((TYPE_SWORD, 'Sword'), (TYPE_AXE, 'Axe'), (TYPE_KNIVE, 'Knive'), 
             (TYPE_CLUBS, 'Clubs'), (TYPE_SHIELD, 'Shield'), 
             (TYPE_HELMET, 'Helmet'), (TYPE_KOLCHUGA, 'Kolchuga'), 
             (TYPE_ARMOR, 'Armor'), (TYPE_BELT, 'Belt'), (TYPE_PANTS, 'Pants'), 
             (TYPE_TREETOP, 'Treetop'), (TYPE_GLOVE, 'Glove'), 
             (TYPE_BOOT, 'Boot'), (TYPE_RING, 'Ring'), (TYPE_AMULET, 'Amulet'), 
             (TYPE_POTION, 'Potion'), (TYPE_ELIXIR, 'Elixir'),)
    
    name = models.CharField(max_length=32, unique=True)
    type = models.IntegerField(choices=TYPES)
    price = models.FloatField()
    
    is_art = models.BooleanField()
    is_bot = models.BooleanField()
    stability = models.IntegerField()
    weight = models.IntegerField()
    image = models.ImageField(upload_to='upload/thing_image')
    
    level_need = models.IntegerField()

    strength_need = models.IntegerField(default=0)
    dexterity_need = models.IntegerField(default=0)
    intuition_need = models.IntegerField(default=0)
    health_need  = models.IntegerField(default=0)
    
    swords_need = models.IntegerField(default=0)
    axes_need = models.IntegerField(default=0)
    knives_need = models.IntegerField(default=0)
    clubs_need = models.IntegerField(default=0)
    shields_need = models.IntegerField(default=0)
    
    strength_give = models.IntegerField(default=0)
    dexterity_give = models.IntegerField(default=0)
    intuition_give = models.IntegerField(default=0)
    health_give = models.IntegerField(default=0)
    
    swords_give = models.IntegerField(default=0)
    axes_give = models.IntegerField(default=0)
    knives_give = models.IntegerField(default=0)
    clubs_give = models.IntegerField(default=0)
    shields_give = models.IntegerField(default=0)
    
    damage_min = models.IntegerField(default=0)
    damage_max = models.IntegerField(default=0)
    
    protection_head = models.IntegerField(default=0)
    protection_breast = models.IntegerField(default=0)
    protection_zone = models.IntegerField(default=0)
    protection_legs = models.IntegerField(default=0)
    
    accuracy = models.IntegerField(default=0)
    dodge = models.IntegerField(default=0)
    devastate = models.IntegerField(default=0)
    durability = models.IntegerField(default=0)
    block_break = models.IntegerField(default=0)
    armor_break = models.IntegerField(default=0)
    
    hp = models.IntegerField(default=0)
    
    time_duration = models.IntegerField(default=0)
    
    strike_count = models.IntegerField(default=0)
    block_count = models.IntegerField(default=0)
    
    capacity = models.IntegerField(default=0)
    
    take_two_hands = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'Thing'
    
    def __unicode__(self):
        return '%s [%s]' % (self.name, self.level_need)
    
    def thumbnail(self):
        url = '%s%s' % (settings.MEDIA_URL, self.image)
        return '<img src="%s" width="%s" height="%s" />' % (url, '', '')
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True
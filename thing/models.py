from django.db import models
from django.conf import settings

class Thing(models.Model):
    name = models.CharField(max_length=32, unique=True)
#
    TYPES = ((0, 'Sword'), (1, 'Axe'), (2, 'Knive'), (3, 'Clubs'), 
            (4, 'Shield'), (5, 'Helmet'), (6, 'Kolchuga'),
            (7, 'Armor'), (8, 'Belt'), (9, 'Pant'), (10, 'Treetop'),
            (11, 'Glove'), (12, 'Boot'), (13, 'Ring'), (14, 'Amulet'),  
            (15, 'Potion'), (16, 'Elixir'),)
    type = models.IntegerField(default=0, choices=TYPES)
    is_art = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False)
    stability = models.IntegerField()
    image = models.ImageField(upload_to='upload/things')
    
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
    protection_leg = models.IntegerField(default=0)
    
    accuracy = models.IntegerField(default=0)
    dodge = models.IntegerField(default=0)
    devastate = models.IntegerField(default=0)
    durability = models.IntegerField(default=0)
    block_break = models.IntegerField(default=0)
    armor_break = models.IntegerField(default=0)
    
    hp = models.IntegerField(default=0)
    
    time_duration = models.IntegerField(default=0)
    
    strike_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'Thing'
    
    def __unicode__(self):
        return '%s [%s]' % (self.name, self.level_need)
    
    def thumbnail(self):
        url = '%s%s' % (settings.MEDIA_URL, self.image)
        return '<img src="%s" width="%s" height="%s" />' % (url, '', '')
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True
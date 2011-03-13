from django.db import models
from django.conf import settings

from thing.models import Thing

class BotImage(models.Model):
    image = models.ImageField(upload_to='upload/botimages')
    
    class Meta:
        db_table = 'BotImage'
        
    def __unicode__(self):
        return str(self.image).split('/')[-1]
        
    def thumbnail(self):
        url = '%s%s' % (settings.MEDIA_URL, self.image)
        return '<img src="%s" width="%s" height="%s" />' % (url, '', '')
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True
           
class Bot(models.Model):
    name = models.CharField(max_length=32, unique=True)
    level = models.IntegerField(default=0)
    image = models.ForeignKey(BotImage, null=True, blank=True)  
    
    hp = models.IntegerField(default=20)

    strength = models.IntegerField(default=3)
    dexterity = models.IntegerField(default=3)
    intuition = models.IntegerField(default=3)
    health = models.IntegerField(default=3)
    
    swords = models.IntegerField(default=0)
    axes = models.IntegerField(default=0)
    knives = models.IntegerField(default=0)
    clubs = models.IntegerField(default=0)
    shields = models.IntegerField(default=0)

    coordinate_x1 = models.IntegerField(default=0)
    coordinate_y1 = models.IntegerField(default=0)
    coordinate_x2 = models.IntegerField(default=0)
    coordinate_y2 = models.IntegerField(default=0)
    
    things = models.ManyToManyField(Thing, null=True, blank=True)
    
    class Meta:
        db_table = 'Bot'
    
    def __unicode__(self):
        return '%s [%s]' % (self.name, self.level)
    
class BotFeature(models.Model):
    bot = models.ForeignKey(Bot)
       
    strength = models.CharField(max_length=32, null=True)
    dexterity = models.CharField(max_length=32, null=True)
    intuition = models.CharField(max_length=32, null=True)
    health = models.CharField(max_length=32, null=True)
    
    swords = models.CharField(max_length=32, null=True)
    axes = models.CharField(max_length=32, null=True)
    knives = models.CharField(max_length=32, null=True)
    clubs = models.CharField(max_length=32, null=True)
    shields = models.CharField(max_length=32, null=True)
    
    protection_head = models.CharField(max_length=32, null=True)
    protection_breast = models.CharField(max_length=32, null=True)
    protection_zone = models.CharField(max_length=32, null=True)
    protection_legs = models.CharField(max_length=32, null=True)
    
    damage_min = models.CharField(max_length=32, null=True)
    damage_max = models.CharField(max_length=32, null=True)
    
    accuracy = models.CharField(max_length=32, null=True)
    dodge = models.CharField(max_length=32, null=True)
    devastate = models.CharField(max_length=32, null=True)
    durability = models.CharField(max_length=32, null=True)
    block_break = models.CharField(max_length=32, null=True)
    armor_break = models.CharField(max_length=32, null=True)
    
    hp = models.CharField(max_length=32, null=True)

    class Meta:
        db_table = 'BotFeature'
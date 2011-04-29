from django.db import models

from building.models import Building
from hero.models import HeroThing

class BuildingCommission(models.Model):
    building = models.ForeignKey(Building, unique=True)
    percent = models.FloatField()
    
    class Meta:
        db_table = 'BuildingCommission'
    
    def __unicode__(self):
        return '%s %s%%' % (self.building, self.percent)


class BuildingCommissionHeroThing(models.Model):
    building = models.ForeignKey(Building)
    herothing = models.ForeignKey(HeroThing)
    price = models.FloatField()

    def thing(self):
        return self.herothing.thing
    
    def hero(self):
        return self.herothing.hero
        
    class Meta:
        db_table = 'BuildingCommissionHeroThing'
        unique_together = (('building', 'herothing'),)

    def __unicode__(self):
        return '%s %s' % (self.building, self.herothing)

from django.db import models

from building.models import Building
from hero.models import Hero

class BuildingSmithy(models.Model):
    building = models.ForeignKey(Building, unique=True)
    percent_repair_money = models.FloatField()
    percent_broken = models.FloatField()
    
    class Meta:
        db_table = 'BuildingSmithy'
    
    def __unicode__(self):
        return '%s %s%%' % (self.building, self.percent_repair_money)

class BuildingSmithyFeature(models.Model):
    buildingsmithy = models.ForeignKey(BuildingSmithy)
    feature = models.IntegerField(choices=Hero.FEATURES)
    plus = models.IntegerField()
    money = models.FloatField()
    
    class Meta:
        db_table = 'BuildingSmithyFeature'
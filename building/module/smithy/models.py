from django.db import models

from building.models import Building
from hero.models import Hero

##
class BuildingSmithy(models.Model):
    building = models.ForeignKey(Building, unique=True)
    percent_repair_money = models.FloatField(default=0.50)
    percent_broken = models.FloatField(default=2.00)
    
    class Meta:
        db_table = 'BuildingSmithy'
    
    def __unicode__(self):
        return '%s %s%%' % (self.building.name, self.percent_repair_money)

class BuildingSmithyFeature(models.Model):
    smithybuilding = models.ForeignKey(BuildingSmithy)
    feature = models.IntegerField(default=0, choices=Hero.FEATURES)
    plus = models.IntegerField()
    money = models.FloatField()
    
    class Meta:
        db_table = 'BuildingSmithyFeature'
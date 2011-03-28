from django.db import models

from building.models import Building

##
class BuildingBuyingup(models.Model):
    building = models.ForeignKey(Building, unique=True)
    percent = models.FloatField(default=10.00)
    
    class Meta:
        db_table = 'BuildingBuyingup'
    
    def __unicode__(self):
        return '%s %s%%' % (self.building.name, self.percent)

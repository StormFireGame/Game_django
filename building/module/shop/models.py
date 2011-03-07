from django.db import models

from building.models import Building
from thing.models import Thing

class BuildingShopThing(models.Model):
    building = models.ForeignKey(Building)
    thing = models.ForeignKey(Thing)
    price = models.FloatField(default=0.00)
    count = models.IntegerField()
    
    class Meta:
        db_table = 'BuildingShopThing'
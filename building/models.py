from django.db import models

class Building(models.Model):
    
    parent = models.IntegerField()
    name = models.CharField(max_length=32)
    module = models.CharField(max_length=32, null=True, blank=True)
    
    coordinate_x1 = models.IntegerField(default=0)
    coordinate_y1 = models.IntegerField(default=0)
    coordinate_x2 = models.IntegerField(default=0)
    coordinate_y2 = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'Building'
    
    def __unicode__(self):
        return self.name
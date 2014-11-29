from django.db import models
from django.conf import settings

from island.models import Island

class Building(models.Model):
    island = models.ForeignKey(Island, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    default_child = models.BooleanField(default=False)
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32, unique=True)
    module = models.CharField(max_length=32, null=True, blank=True)
    image = models.FileField(upload_to='upload/building_image', null=True,
                              blank=True)
    
    coordinate_x1 = models.IntegerField(null=True, blank=True)
    coordinate_y1 = models.IntegerField(null=True, blank=True)
    coordinate_x2 = models.IntegerField(null=True, blank=True)
    coordinate_y2 = models.IntegerField(null=True, blank=True)
        
    class Meta:
        db_table = 'Building'
    
    def __unicode__(self):
        return self.name
    
    def thumbnail(self):
        url = '%s%s' % (settings.MEDIA_URL, self.image)
        return '<img src="%s" width="%s" height="%s" />' % (url, '', '')
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True

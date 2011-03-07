from django.db import models
from django.conf import settings

class Building(models.Model):
    parent = models.ForeignKey('self', null=True, blank=True)
    default_child = models.BooleanField(default=False)
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=32, unique=True)
    plugin = models.CharField(max_length=32, null=True, blank=True)
    image = models.ImageField(upload_to='upload/buildingimages', null=True, 
                              blank=True)
    
    coordinate_x1 = models.IntegerField(default=0)
    coordinate_y1 = models.IntegerField(default=0)
    coordinate_x2 = models.IntegerField(default=0)
    coordinate_y2 = models.IntegerField(default=0)
        
    class Meta:
        db_table = 'Building'
    
    def __unicode__(self):
        return self.name
    
    def thumbnail(self):
        url = '%s%s' % (settings.MEDIA_URL, self.image)
        return '<img src="%s" width="%s" height="%s" />' % (url, '', '')
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True
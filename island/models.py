from django.db import models

from django.conf import settings

class Island(models.Model):
    name = models.CharField(max_length=32, unique=True)
    slug = models.SlugField(max_length=32, unique=True)
    image = models.FileField(upload_to='upload/island_image')
    
    class Meta:
        db_table = 'Island'
    
    def __unicode__(self):
        return self.name

class IslandPart(models.Model):
    island = models.ForeignKey(Island)
    is_move = models.BooleanField(default=False)
    coordinate_x = models.IntegerField()
    coordinate_y = models.IntegerField()
    
    class Meta:
        db_table = 'IslandPart'
        unique_together = (('island', 'coordinate_x', 'coordinate_y'),)
        
    def __unicode__(self):
        return 'Coordinate %s %s' % (self.coordinate_x, self.coordinate_y)
        
    def thumbnail(self):
        url = '%s%s' % (settings.MEDIA_URL, self.image)
        return '<img src="%s" width="%s" height="%s" />' % (url, '', '')
    thumbnail.short_description = 'Image'
    thumbnail.allow_tags = True

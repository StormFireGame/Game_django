from django.db import models

class TableExperience(models.Model):
    level = models.IntegerField()
    experience = models.IntegerField()
    coefficient = models.FloatField()
    number_of_abilities = models.IntegerField()
    number_of_skills = models.IntegerField()
    number_of_parameters = models.IntegerField()
    money = models.FloatField()
    
    class Meta:
        db_table = 'TableExperience'
    
    def __unicode__(self):
        return str(self.level)
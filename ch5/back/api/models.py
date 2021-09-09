from django.db import models

class RandomForest(models.Model):
    gest = models.IntegerField()
    birthweight = models.FloatField()
    MAS = models.BooleanField()
    gender = models.BooleanField()
    multip = models.BooleanField()
    level_3 = models.BooleanField()

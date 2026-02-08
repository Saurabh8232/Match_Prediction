from django.db import models

# Create your models here.

class DummyData(models.Model):
    Age = models.IntegerField()
    Gender = models.IntegerField()
    HeartRate = models.IntegerField()
    SystolicBloodPressure = models.IntegerField()
    DiastolicBloodPressure = models.IntegerField()
    BloodSugar = models.FloatField()
    CK_MB = models.FloatField()
    Troponin = models.FloatField()

    def __str__(self):
        return self.Age
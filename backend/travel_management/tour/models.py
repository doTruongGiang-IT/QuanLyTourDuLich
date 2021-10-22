from django.db import models


class LocationType(object):
    ABOARD  = "Aboard"
    DOMESTIC = "Domestic"
    UNKNOWN = "Unknown"
    CHOICES = [
        (ABOARD, ABOARD),
        (DOMESTIC, DOMESTIC),
        (UNKNOWN, UNKNOWN),
    ]
    
    
class TourCharacteristic(models.Model):
    name                = models.TextField()
    
    def __str__(self):
        return f"{self.id} | {self.name}" 


class TourType(models.Model):
    name                = models.TextField()
    
    def __str__(self):
        return f"{self.id} | {self.name}" 


class TourPrice(models.Model):
    name                = models.TextField()
    price               = models.IntegerField()
    start_date          = models.DateField()
    end_date            = models.DateField()
    
    def __str__(self):
        return f"{self.id} | {self.name}" 


class Location(models.Model):
    name                = models.TextField()
    type                = models.CharField(
                            max_length=10,
                            choices=LocationType.CHOICES,
                            default=LocationType.UNKNOWN,
                        )
    
    def __str__(self):
        return f"{self.id} | {self.name}" 


class Tour(models.Model):
    name                = models.TextField()
    characteristic      = models.ForeignKey(TourCharacteristic, on_delete=models.CASCADE)
    type                = models.ForeignKey(TourType, on_delete=models.CASCADE)
    price               = models.ForeignKey(TourPrice, on_delete=models.CASCADE)
    location            = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id} | {self.name}" 

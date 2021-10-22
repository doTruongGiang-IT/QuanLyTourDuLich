from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from tour.models import Tour, Location


class Group(models.Model):
    name                = models.TextField()
    tour                = models.ForeignKey(Tour, on_delete=models.CASCADE)
    start_date          = models.DateField()
    end_date            = models.DateField()
    revenue             = models.IntegerField(default=0)
    
    def clean(self):
        errors = {}
        
        if self.start_date > self.end_date:
            errors['end_date']= _('end_date is invalid')
            
        if errors:
            raise ValidationError(errors)
    
    def __str__(self):
        return f"{self.id} | {self.name} | {self.tour}" 


class GroupJourney(models.Model):
    group               = models.ForeignKey(Group, on_delete=models.CASCADE)
    content             = models.TextField()
    start_date          = models.DateTimeField()
    end_date            = models.DateTimeField()
    location            = models.ForeignKey(Location, on_delete=models.CASCADE)
    
    def clean(self):
        errors = {}
        
        if self.start_date > self.end_date:
            errors['end_date']= _('end_date is invalid')
            
        if errors:
            raise ValidationError(errors)
    
    def __str__(self):
        return f"{self.id} | {self.group} | {self.content[:50]}" 
from django.db import models
from group.models import Group

class GroupGenderType(object):
    MALE  = "Male"
    FEMALE = "Female"
    UNKNOWN = "Unknown"
    CHOICES = [
        (MALE, MALE),
        (FEMALE, FEMALE),
        (UNKNOWN, UNKNOWN),
    ]
    
class Customer(models.Model):
    name                = models.TextField()
    id_number           = models.TextField(unique=True)
    address             = models.TextField()
    gender              = models.CharField(
                            max_length=20,
                            choices=GroupGenderType.CHOICES,
                            default=GroupGenderType.UNKNOWN,
                        )
    phone_number        = models.TextField()
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.id} | {self.name}" 
    
    
class GroupCustomer(models.Model):
    group               = models.ForeignKey(Group, on_delete=models.CASCADE)
    customer            = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['id']
        unique_together = ['group', 'customer']

    def __str__(self):
        return f"{self.group} | {self.customer}" 
from django.db import models
from group.models import Group
    
    
class Staff(models.Model):
    name                = models.TextField()
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.id} | {self.name}" 
    
    
class StaffType(models.Model):
    name                = models.TextField()
    
    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.id} | {self.name}" 
    
    
class GroupStaff(models.Model):
    group               = models.ForeignKey(Group, on_delete=models.CASCADE)
    staff               = models.ForeignKey(Staff, on_delete=models.CASCADE)
    staff_type          = models.ForeignKey(StaffType, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['id']
        unique_together = ['group', 'staff']

    def __str__(self):
        return f"{self.group} | {self.staff}" 
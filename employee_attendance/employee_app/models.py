from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Employee(models.Model):
    employee_name   = models.OneToOneField(User,on_delete=models.CASCADE, related_name='employee')
    in_time         = models.DateTimeField(blank=True,null=True)
    out_time        = models.DateTimeField(blank=True,null=True)
    status          = models.BooleanField(default=False)

    def __str__(self):
        return self.employee_name.username

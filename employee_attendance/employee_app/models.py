from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EmployeeAttendanceRecord(models.Model):
    employees       = models.ForeignKey(User,on_delete=models.CASCADE, related_name='employee_records')
    in_time         = models.DateTimeField(blank=True,null=True)
    out_time        = models.DateTimeField(blank=True,null=True)
    status          = models.BooleanField(default=False)
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.employees.username

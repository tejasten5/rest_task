from django.core.management.base import BaseCommand
from django.utils import timezone
from employee_app.models import *

class Command(BaseCommand):
    help = "Reset all employess data as per date changes.Set to crown job.Can be executed at midnight every day."

    def handle(self, *args, **kwargs):
        try:
            
            for user in User.objects.all():                
                EmployeeAttendanceRecord.objects.create(
                    employees = user
                )
        except Exception as e:
            print(e)

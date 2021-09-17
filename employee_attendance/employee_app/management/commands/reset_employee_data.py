from django.core.management.base import BaseCommand
from django.utils import timezone
from employee_app.models import *

class Command(BaseCommand):
    help = "Reset all employess data as per date changes.Set to crown job.Can be executed at midnight every day."

    def handle(self, *args, **kwargs):
        try:
            Employee.objects.all().update(status = False)
        except Exception as e:
            self.stdout.write(self.style.WARNING(str(e)))

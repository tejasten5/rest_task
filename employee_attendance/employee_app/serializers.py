from employee_app.models import EmployeeAttendanceRecord
from rest_framework import serializers



class EmployeeSerializer(serializers.ModelSerializer):        
    """This serializer is used for Device module.
    """
    class Meta:
        model = EmployeeAttendanceRecord
        fields = '__all__'

   
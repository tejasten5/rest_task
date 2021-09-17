from employee_app.models import Employee
from rest_framework import serializers



class EmployeeSerializer(serializers.ModelSerializer):        
    """This serializer is used for Device module.
    """
    class Meta:
        model = Employee
        fields = '__all__'

   
from django import forms
from .models import *
from django.core.exceptions import ValidationError

class AddEmployeeForm(forms.Form):    
    username                = forms.CharField(required = True,strip = True)
    password                = forms.CharField(max_length=50,required=True,strip=True)
    confirm_password        = forms.CharField(max_length=500,required=True,strip=True)

    

    def clean(self):
        cleaned_data = super(AddEmployeeForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        username=cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError({"username":"Username already exists.Please use a different username."})

        if password != confirm_password:
            raise ValidationError(
                {"confirm_password":"Passwords does not match."}
            )


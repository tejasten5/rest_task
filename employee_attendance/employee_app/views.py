from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404,render
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.decorators import (
    action
) 
from django.contrib import messages

from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from ast import literal_eval
from django.views.generic import TemplateView
from .forms import *
from .serializers import *
from . import convert_to_pdf
from django.views.generic import View
# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.http import (HttpResponseRedirect,
                         JsonResponse,
                         HttpResponse,
                         Http404,)
from django.urls import reverse_lazy, reverse

# token = Token.objects.create(user=...)

SERVER_ERROR = {"error":"Something went wrong ! Please contact techinical team."}

class LoginTemplateView(TemplateView):
    template_name = 'login.html'

class HomeTemplateView(LoginRequiredMixin,TemplateView):
    template_name = 'home.html'


class AdminLogin(View):
    def post(self,request):
        print(request.POST,'LLL')
        if request.user.is_authenticated:
            return HttpResponseRedirect('/home/')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)                    
                    return HttpResponseRedirect('/home/')
            messages.error(request, "Sorry, that didn't work. Please try again")
        return render(request, 'login.html', {})

class LogoutView(View):
    def get(self, request):  
          
        if request.user.is_authenticated:
            user = request.user            
            user.save()
        logout(request)
        return HttpResponseRedirect('/')

class EmployeeListAPI(LoginRequiredMixin,viewsets.ModelViewSet):   
    queryset = User.objects.all()
    serializer_class = EmployeeSerializer

    def get_object(self,*args,**kwargs):        
        return get_object_or_404(User,**kwargs)

    def get_initial_query(self):        
        return Employee.objects.filter(employee_name__is_superuser = False)

    def get_ordered_query(self, user_query, request):        
        column_index    = request.POST.get("order[0][column]")
        order_dir       = request.POST.get("order[0][dir]", "")
        column_name     = request.POST.get(f"columns[{column_index}][data]")
        
        if column_name:
            prefix = "" if order_dir == "asc" else "-"
            return user_query.order_by(f"{prefix}{column_name}")
        return user_query

    def get_filtered_query(self, user_query, request):        
        searched_value = request.POST.get("search[value]", "").lower()  
             

        return user_query.filter(
                Q(employee_name__username__icontains=searched_value)|
                Q(in_time__icontains=searched_value)|Q(out_time__icontains = searched_value)|Q(status__icontains = searched_value)
            )

    def format_paginated_query(self, users_list, request):        
        user_data = []
        row_number = users_list.start_index()
        for user in  users_list:
            user_data.append({
                "srno":row_number,
                'employee_name':user["employee_name__username"],
                'in_time':user["in_time"].strftime('%H:%M:%S') if user["in_time"] else "NA",
                'out_time':user["out_time"].strftime('%H:%M:%S') if user["out_time"] else "NA",
                "status":f'<span class="badge badge-success">Present</span>' if user["status"] else f'<span class="badge badge-danger">Absent</span>',
                "in_btn":f"<button  class='btn btn-success in_btn_class' data-id='{user['id']}'>IN</button>",
                "out_btn":f"<button  class='btn btn-danger out_btn_class' data-id='{user['id']}'>OUT</button>"
            })   
            row_number += 1
        return user_data

    

    
    
    @action(detail=False, methods=['POST'])
    def get_list(self,request): 
        try:
            
            start = literal_eval(request.POST.get("start", "0"))
            length = literal_eval(request.POST.get("length", "10"))

            initial_query = self.get_initial_query()
            filtered_location_query = self.get_filtered_query(initial_query, request)
            user_query = self.get_ordered_query(filtered_location_query, request)

            page = int(start/length) + 1
            paginator = Paginator(
                            user_query.values('id','employee_name__username','in_time','out_time','status'), 
                            length,
                        )

            try:
                employee_list = paginator.page(page)
            except PageNotAnInteger:
                employee_list = paginator.page(1)
            except EmptyPage:
                employee_list = paginator.page(paginator.num_pages)

            user_data = self.format_paginated_query(employee_list, request)

            data = {
            "data": user_data,
            "recordsTotal": initial_query.count(),   
            "recordsFiltered": user_query.count(),    
            "present_emp":initial_query.filter(status = True).count(),
            "absent_emp":initial_query.filter(status = False).count()
            }     
            return Response(data,status = 200)
        except Exception as e:
            print(str(e))
            return Response(SERVER_ERROR,status = 500)    
        
    @action(detail=False, methods=['POST'])
    def create_employee(self,request):                       
        try:
            form = AddEmployeeForm(request.POST)
            if form.is_valid():
                username = form.cleaned_data.get("username")              
                password = form.cleaned_data.get("password")
                confirm_password = form.cleaned_data.get("confirm_password")
                
                user_obj = User.objects.create(
                    username = username,
                    is_superuser = False,
                    is_staff = False,
                    is_active = True
                )
                user_obj.set_password(confirm_password)                               
                user_obj.save()

                Employee.objects.create(
                    employee_name = user_obj
                )
                return Response({"status":"OK"},status = 201)            
            return Response(form.errors,status = 400)            
        except Exception as e:
            print(str(e))
            return Response(SERVER_ERROR,status = 500)    

    @action(detail=False, methods=['POST'])
    def update_time(self,request):
        time_status = ''
        try:             
            flag = request.POST.get('flag')           
            userid = request.POST.get('user_id')
            emp_obj = Employee.objects.filter(id = userid)
            
            if emp_obj.exists():
                if flag == "INTIME":
                    emp_obj.update(
                        in_time = timezone.now()
                    )
                    time_status = 'In-Time'
                elif flag == "OUTTIME":
                    
                    if emp_obj.first().in_time:
                        emp_obj.update(
                            out_time = timezone.now(),
                            status = True
                        )
                        time_status = 'Out-Time'
                    else:
                        return Response({"error":"Set IN-Time of employee."},status = 400)                
                return Response({"time_status":time_status},status = 200)
            return Response({"error":"User does not exists."},status = 400)
        except Exception as e:
            print(str(e))
            return Response(SERVER_ERROR,status = 500)


    def export_pdf(self,request):
        try:
            template_path = 'employee_pdf.html'
            employe_list = []

            for employee in Employee.objects.values('id','employee_name__username','status','in_time','out_time'):
                employe_list.append({
                    'id':employee["id"],
                    'name':employee["employee_name__username"],
                    'in_time':employee["in_time"].strftime('%H:%M:%S') if employee["in_time"] else '--',
                    'out_time':employee["out_time"].strftime('%H:%M:%S') if employee["out_time"] else '--',
                    "status":"Present" if employee["status"] else "Absent"
                })


            context = {"employees":employe_list,"today":timezone.now().strftime('%Y-%m-%d')}
            pdf = convert_to_pdf.render_to_pdf(template_path, context)
            response = HttpResponse(pdf, content_type='application/pdf')
            return response
        except Exception as e:
            print(str(e))
            return Response(SERVER_ERROR,status = 500)

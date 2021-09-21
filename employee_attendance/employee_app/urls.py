from django.urls import path
from .views import *
urlpatterns = [
    path('',LoginTemplateView.as_view(),name= "login"),
    path('home/',HomeTemplateView.as_view(),name="home"),


    #api
    path('api/add_employee/',EmployeeListAPI.as_view({'post':'create_employee'}),name="create_employee"),
    path('api/employee_list/',EmployeeListAPI.as_view({'post':'get_list'}),name="list_employee"),
    path('api/export_pdf/',EmployeeListAPI.as_view({'post':'export_pdf'}),name="export_pdf"),
    path('update_time/',EmployeeListAPI.as_view({'post':'update_time'}),name="update_time"),
    path('login/',AdminLogin.as_view(),name="login1"),
    path('logout/',LogoutView.as_view(),name="logout")
]

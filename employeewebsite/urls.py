from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="home"),
    path('departments/', views.department_list, name='department_list'),
    path('departments/<int:department_id>/', views.department_detail, name='department_detail'),

    path('roles/', views.role_list, name='role_list'),
    path('roles/<int:role_id>/', views.role_detail, name='role_detail'),

    path('employees/', views.employee_list, name='employee_list'),
    path('employees/<int:employee_id>/', views.employee_detail, name='employee_detail'),
    path('employees/add/', views.employee_add, name='employee_add'),
    path('role/add/', views.role_add, name='role_add'),
    path('department/add/', views.department_add, name='department_add'),
    path('employees/<int:employee_id>/update/', views.employee_update, name='employee_update'),
    path('employees/<int:employee_id>/delete/', views.employee_delete, name='employee_delete'),
]

from django.urls import path, include
from . import views


urlpatterns = [             
    path('register', views.register, name="register"),
    path('create_super_user', views.register, name="create_superuser"),
    path('create_staff_user', views.register, name="create_staffuser"),
    path('', views.home, name="main-home"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('activate/<str:uidb64>/<str:token>/', views.activate_user, name='activate_user'),
    path('employeewebsite/home/', views.employee_home_view, name='employee-home'),

]

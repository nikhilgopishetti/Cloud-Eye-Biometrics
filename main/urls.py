from django.urls import path, include
from . import views


urlpatterns = [             
    path('register', views.register, name="register"),
    path('create_super_user', views.create_superuser, name="create_superuser"),
    path('create_staff_user', views.create_staff_user, name="create_staffuser"),
    path('', views.home, name="main-home"),
    path('process_image/', views.process_image, name='process_image'),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('activate/<str:uidb64>/<str:token>/', views.activate_user, name='activate_user'),
    path('upload/', views.upload_image, name='upload_image'),
    path('adminDashboard/', views.user_activity_log, name='user_activity_log'),
    path('employeewebsite/home/', views.employee_home_view, name='employee-home'),

]

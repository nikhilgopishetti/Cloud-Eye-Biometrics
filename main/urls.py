from django.urls import path, include
from . import views


urlpatterns = [             
    path('register', views.register, name="register"),
    path('create_super_user', views.register, name="create_superuser"),
    path('create_staff_user', views.register, name="create_staffuser"),
    path('', views.home, name="main-home"),
    path('process_image/', views.process_image, name='process_image'),
    path('display_photo/', views.display_photo, name='display_photo'),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('activate/<str:uidb64>/<str:token>/', views.activate_user, name='activate_user'),
    path('display-images/', views.display_images, name='display_images'),
    path('employeewebsite/home/', views.employee_home_view, name='employee-home'),

]

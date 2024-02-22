from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User
from .models import AbnormalBehavior, UserActivityLog
from main.behaviour import monitor_mouse_behavior, monitor_typing_speed
from .utils import generate_token, send_activation_email, activate_user
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import ImageUploadForm
from .forms import ImageForm
from .decorators import *
from django.contrib.auth.decorators import user_passes_test
from .photoscript import authenticateimage
import boto3
import os
from PIL import Image
import io
import time

@superuser_required
def create_staff_user(request):
    logout = logout(request)
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Create a staff user
        User.objects.create_user(username=username, email=email, password=password, is_staff=True)
        activitylog = UserActivityLog.objects.create(
            user=request.user,
            activity_type='Create User',
            details='Staff User Created'
        )
        activitylog.save()

        messages.success(request, f'Staff user {username} created successfully!')
        return redirect('home')  # Redirect to home or another appropriate URL

    return render(request, 'main/createstaffuser.html') 

@superuser_required
def create_superuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Check if a user with the given username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Try another username.')
            return redirect('create_superuser')  # Redirect to the same page

        # Create a superuser
        User.objects.create_superuser(username=username, email=email, password=password)
        activitylog = UserActivityLog.objects.create(
            user=request.user,
            activity_type='Create User',
            details='Super User Created'
        )
        activitylog.save()

        messages.success(request, f'Superuser {username} has been created successfully!')
        return redirect('home')  # Redirect to the home page or admin panel

    return render(request, 'main/createsuperuser.html')

@logout_required
def login_user(request):

    abnormalmouseinstance = monitor_mouse_behavior()
    abnormalkeyboardinstance = monitor_typing_speed()   
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            activitylog = UserActivityLog.objects.create(
                user=request.user,
                activity_type='Login',
                details='User logged in'
            )
            activitylog.save()
            messages.success(request, f'Welcome, {user.username}!')
            return redirect('main-home')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'main/login.html')


def register(request):
    if request.method == "POST":
        context = {'has_error': False, 'data': request.POST}
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if len(password) < 6:
            messages.add_message(request, messages.ERROR, 'Password should be at least 6 characters')
            context['has_error'] = True

        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.ERROR, 'Username is taken, choose another one')
            context['has_error'] = True

        if User.objects.filter(email=email).exists():
            messages.add_message(request, messages.ERROR, 'Email is taken, choose another one')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'main/register.html', context)

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        activitylog = UserActivityLog.objects.create(
            user=request.user,
            activity_type='Registration',
            details='New User Registered'
        )
        activitylog.save()
        send_activation_email(user, request)

        messages.add_message(request, messages.SUCCESS, 'We sent you an email to verify your account')

    return render(request, 'main/register.html')


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['image']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            file_extension = os.path.splitext(file.name)[1].lower()  # Get the file extension
            
            # Rename the file
            new_filename = f"{first_name}_{last_name}{file_extension}"
            print(new_filename)
            
            # Create a temporary file with the new filename
            with open(new_filename, 'wb+') as new_file:
                for chunk in file.chunks():
                    new_file.write(chunk)
            
            bucket_name = 'biometricsplus-employees-images'
            object_name = new_filename
            
            s3_client = boto3.client('s3')
            try:
                # Upload the renamed file
                with open(new_filename, 'rb') as file_data:
                    s3_client.upload_fileobj(file_data, bucket_name, object_name)
                os.remove(new_filename)  # Remove the temporary file
                activitylog = UserActivityLog.objects.create(
                    user=request.user,
                    activity_type='Registration',
                    details='New user Registered with image'
                )
                activitylog.save()
                return redirect('login')  
            except Exception as e:
                # Handle upload failure
                print(f"Upload failed: {e}")
                return render(request, 'main/upload.html', {'form': form, 'error_message': 'Upload failed. Please try again.'})
    else:
        form = ImageUploadForm()
    return render(request, 'main/upload.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'main/home.html')

@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def employee_home_view(request):
    return render(request, 'employeewebsite/home.html')

def shoeapp(request):
    return render(request, 'base/home.html')


@csrf_exempt
def process_image(request):
    if request.method == 'POST':
        try:
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                # Access the uploaded image directly
                uploaded_image = request.FILES['image']
                
                # Process the image file as needed
                image_folder = 'testimages'  # Specify the path to your folder
                image_path = os.path.join(image_folder, uploaded_image.name)

                with open(image_path, 'wb') as f:
                    for chunk in uploaded_image.chunks():
                        f.write(chunk)
                                

                print(image_path)
                rekognition = boto3.client('rekognition', region_name='us-east-1')
                dynamodb = boto3.client('dynamodb', region_name='us-east-1')

            

                image = Image.open(image_path)
                stream = io.BytesIO()
                image.save(stream,format="PNG")
                image_binary = stream.getvalue()


                response = rekognition.search_faces_by_image(
                        CollectionId='employees-images',
                        Image={'Bytes':image_binary}                                       
                        )

                found = False
                for match in response['FaceMatches']:
                    print (match['Face']['FaceId'],match['Face']['Confidence'])
                        
                    face = dynamodb.get_item(
                        TableName='employees',  
                        Key={'rekognitionid': {'S': match['Face']['FaceId']}}
                        )
                    
                    if 'Item' in face:
                        print ("Found Person: ",face['Item']['firstName']['S'])
                        found = True
                        user, created = User.objects.get_or_create(username=face['Item']['lastName']['S'])
                        if created:
                            user.set_unusable_password()
                            user.save()
                        login(request, user)  # Log in the user
                        activitylog = UserActivityLog.objects.create(
                            user=request.user,
                            activity_type='Login',
                            details='User logged in with Image'
                        )
                        activitylog.save()
                        print("the user is logged in as "+ user.username)
                        return redirect('main-home')
                        
                    return HttpResponse(status=204)   

                if not found:
                    print("Person cannot be recognized")
        except Exception as e:
            # Handle any exceptions that may occur during image processing
            print(e)
    return render(request, 'main/photo.html')


def user_activity_log(request):
    user_activity_logs = UserActivityLog.objects.all()
    # Fetch all users from the database
    all_users = User.objects.all()


    # Search functionality
    query = request.GET.get('q')
    if query:
        # Perform case-insensitive search across all user usernames
        all_users = all_users.filter(username__icontains=query)

        # Perform search across all log details
        user_activity_logs = user_activity_logs.filter(user__contains=query)

    context = {
        'all_users': all_users,
        'user_activity_logs': user_activity_logs
    }
    return render(request, 'main/user_activity_log.html', context)
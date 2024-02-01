from django.shortcuts import render, redirect
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth.models import User
from .utils import generate_token, send_activation_email, activate_user
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ImageModel
from .forms import ImageForm
from .photoscript import authenticateimage
import boto3
import os
from PIL import Image
import io
import time

def create_staff_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Create a staff user
        user = User.objects.create_user(username=username, email=email, password=password, is_staff=True)

        messages.success(request, f'Staff user {username} created successfully!')
        return redirect('home')  # Redirect to home or another appropriate URL

    return render(request, 'main/createstaffuser.html') 

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
        user = User.objects.create_superuser(username=username, email=email, password=password)

        messages.success(request, f'Superuser {username} has been created successfully!')
        return redirect('home')  # Redirect to the home page or admin panel

    return render(request, 'main/createsuperuser.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
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

        send_activation_email(user, request)

        messages.add_message(request, messages.SUCCESS, 'We sent you an email to verify your account')

    return render(request, 'main/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'main/home.html')


def employee_home_view(request):
    return render(request, 'employeewebsite/home.html')


def display_photo(request):

    return render(request, 'main/photo.html')

@csrf_exempt  # Add this decorator to exempt CSRF token requirement for simplicity in this example (consider using it properly in production)
def process_image(request):
    if request.method == 'POST':
        try:
            form = ImageForm(request.POST, request.FILES)
            if form.is_valid():
                # Access the uploaded image directly
                uploaded_image = request.FILES['image']
                
                # Process the image file as needed
                # Example: You can pass the image to another script for processing


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
                        user, created = User.objects.get_or_create(username=match['Face']['FaceId'])
                        if created:
                            user.set_unusable_password()
                            user.save()
                        login(request, user)  # Log in the user
                        
                        

                if not found:
                    print("Person cannot be recognized")

                
            response_data = {'status': 'success', 'message': 'Image processed successfully'}

            return JsonResponse(response_data)
        except Exception as e:
            # Handle any exceptions that may occur during image processing
            response_data = {'status': 'error', 'message': str(e)}
            return JsonResponse(response_data, status=500)
    print(response_data)
    # If the request method is not POST, return an error response
    response_data = {'status': 'error', 'message': 'Invalid request method'}
    return render(request, 'main/photo.html')

def display_images(request):
    # Get all images from the ImageModel
    images = ImageModel.objects.all()
    return render(request, 'main/display_images.html', {'images': images})
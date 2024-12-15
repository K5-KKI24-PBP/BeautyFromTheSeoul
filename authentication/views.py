from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from authentication.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from authentication.forms import CustomAuthenticationForm
from authentication.models import User
from django.http import HttpResponse, JsonResponse
from django.core import serializers
import json
from django.views.decorators.csrf import csrf_exempt
from authentication.models import UserProfile

def login_user(request):
    if request.method == "POST":
        form= CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next_page = request.GET.get("next")
                response = redirect(next_page) if next_page else redirect("main:show_main")
                response.set_cookie("user_logged_in", user.username) 
                return response
            else:
                messages.info(request, "Incorrect username or password. Please try again.")
        else:
            messages.info(request, "Incorrect username or password. Please try again.")
    else:
        form = CustomAuthenticationForm()
    context = {'form': form}

    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('user_logged_in')
    return response

def register_user(request):
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("authentication:login")
    context = {"form": form}
    if request.user.is_authenticated:
        return redirect("main:show_main")
    else:
        return render(request, "register.html", context)
    
def get_user(request):
    data = User.objects.all()
    return HttpResponse(serializers.serialize('json', data), content_type='application/json')

@csrf_exempt
def login_flutter(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            try:
                user_profile = user.userprofile 
                role = user_profile.user_role
            except UserProfile.DoesNotExist:
                role = "customer" 
                
            return JsonResponse({
                "status": True,
                "message": "Successfully Logged In!",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.first_name,
                    "role": role
                }
            }, status=200)
        else:
            return JsonResponse({
                "status": False,
                "message": "Login Failed, account is not active"
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Login Failed, wrong username or password"
        }, status=401)

@csrf_exempt
def logout_flutter(request):
    username = request.user.username
    try:
        logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logout successful!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)

@csrf_exempt 
def register_flutter(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            # Extract data from request
            username = data.get('username')
            password = data.get('password')
            email = data.get('email')
            name = data.get('name')
            user_role = data.get('user_role', 'customer')  # Default to customer

            # Validate required fields
            if not all([username, password, email, name]):
                return JsonResponse({
                    "status": False,
                    "message": "Missing required fields"
                }, status=400)

            # Check if username exists
            if User.objects.filter(username=username).exists():
                return JsonResponse({
                    "status": False,
                    "message": "Username already exists"
                }, status=400)

            # Check if email exists
            if User.objects.filter(email=email).exists():
                return JsonResponse({
                    "status": False,
                    "message": "Email already in use"
                }, status=400)

            # Create user
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=name
            )

            # Set permissions based on role
            if user_role == "admin":
                user.is_superuser = True
                user.is_staff = True
                user.save()

            # Create user profile
            UserProfile.objects.create(user=user, user_role=user_role)

            return JsonResponse({
                "status": True,
                "message": "Registration successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "name": user.first_name,
                    "role": user_role
                }
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({
                "status": False,
                "message": "Invalid JSON data"
            }, status=400)
            
        except Exception as e:
            return JsonResponse({
                "status": False,
                "message": str(e)
            }, status=500)

    return JsonResponse({
        "status": False,
        "message": "Invalid request method"
    }, status=405)

def get_user_profile(request, user_id):
    user = User.objects.filter(id=user_id)
    return HttpResponse(serializers.serialize('json', user), content_type='application/json')
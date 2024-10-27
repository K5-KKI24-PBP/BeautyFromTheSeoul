from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from authentication.forms import RegistrationForm
from django.contrib.auth.forms import AuthenticationForm
from authentication.forms import CustomAuthenticationForm

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
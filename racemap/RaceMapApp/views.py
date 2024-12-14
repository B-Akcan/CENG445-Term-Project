from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, MapCreateForm

# Create your views here.

def index(request):
    return render(request, "home.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            name = form.cleaned_data["first_name"]
            surname = form.cleaned_data["last_name"]

            User.objects.create_user(username=username, password=password, first_name=name, last_name=surname)
            
            messages.success(request, f"User {username} was created.")
            return redirect("/accounts/login")
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            messages.error(request, error_string)
        
    return render(request, 'registration/register.html', {'form': RegisterForm})

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect("/")
        else:
            messages.error(request, "Wrong username or password.")

    return render(request, 'registration/login.html', {'form': AuthenticationForm})
    
def logout_view(request):
    if request.method == "POST":
        if request.POST["submit"] == "Logout":
            logout(request)
        return redirect("/")
    return render(request, "registration/logout.html")

@login_required
def create_map(request):
    if request.method == "POST":
        form = MapCreateForm(request.POST)
        if form.is_valid():
            pass
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            messages.error(request, error_string)

    return render(request, "create_map.html", {"form": MapCreateForm})
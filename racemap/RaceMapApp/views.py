from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import  authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, MapCreateForm, ComponentCreateForm, ComponentRotateDeleteForm
from socket import socket, AF_INET, SOCK_STREAM
from .models import Map, ComponentRegistry, Component

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
def components(request):
    if request.method == "POST":
        if request.POST["submit"] == "Register":
            comp_type = request.POST["comp_type"]

            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"REGISTER_COMP {comp_type}\n".encode())
            reply = s.recv(1024).decode()
            s.close()

            comp = ComponentRegistry.objects.get(type=comp_type)
            comp.is_registered = True
            comp.save()

            messages.success(request, reply)
        elif request.POST["submit"] == "Unregister":
            comp_type = request.POST["comp_type"]

            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"UNREGISTER_COMP {comp_type}\n".encode())
            reply = s.recv(1024).decode()
            s.close()

            comp = ComponentRegistry.objects.get(type=comp_type)
            comp.is_registered = False
            comp.save()

            messages.success(request, reply)
        elif request.POST["submit"] == "Register All":
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"REGISTER_ALL_COMPS\n".encode())
            reply = s.recv(1024).decode()
            s.close()

            comps = ComponentRegistry.objects.all()
            for comp in comps:
                comp.is_registered = True
                comp.save()

            messages.success(request, reply)

    registered_comps = ComponentRegistry.objects.filter(is_registered=True)
    unregistered_comps = ComponentRegistry.objects.filter(is_registered=False)
    return render(request, "components.html", {"registered_comps": registered_comps, "unregistered_comps": unregistered_comps})

@login_required
def create_map(request):
    if request.method == "POST":
        form = MapCreateForm(request.POST)
        if form.is_valid():
            num_cols = form.cleaned_data["num_cols"]
            num_rows = form.cleaned_data["num_rows"]
            cellsize = form.cleaned_data["cellsize"]
            bg_color = form.cleaned_data["bg_color"]

            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"CREATE_MAP {num_cols} {num_rows} {cellsize} {bg_color}\n".encode())
            reply = s.recv(1024).decode()
            s.close()

            _id = reply.split()[4]
            m = Map(_id, num_cols, num_rows, cellsize, bg_color)
            m.save()
            m.users.add(User.objects.get(username=request.user))
            m.save()

            messages.success(request, reply)
            return redirect("/racemap/maps")
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            messages.error(request, error_string)

    return render(request, "create_map.html", {"form": MapCreateForm})

@login_required
def maps(request):
    if request.method == "POST":
        if request.POST["submit"] == "View":
            map_id = int(request.POST["map_id"])
            return redirect(f"/racemap/maps/{map_id}")
        
        elif request.POST["submit"] == "Attach":
            map_id = int(request.POST["map_id"])
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"ATTACH_MAP {map_id}\n".encode())
            reply = s.recv(1024).decode()
            s.close()

            Map.objects.get(id=map_id).users.add(
                User.objects.get(username=request.user)
            )

            messages.success(request, reply)
        
        elif request.POST["submit"] == "Detach":
            map_id = int(request.POST["map_id"])
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"DETACH_MAP {map_id}\n".encode())
            reply = s.recv(1024).decode()
            s.close()

            Map.objects.get(id=map_id).users.remove(
                User.objects.get(username=request.user)
            )

            messages.success(request, reply)

        elif request.POST["submit"] == "Delete":
            map_id = int(request.POST["map_id"])

            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"DELETE_MAP {map_id}\n".encode())
            reply = s.recv(1024).decode()
            s.close()

            Map.objects.get(id=map_id).delete()

            messages.success(request, reply)
        
    attached_maps = list(User.objects.get(username=request.user).maps.all())
    unattached_maps = list(Map.objects.exclude(users__username=request.user))
    return render(request, "maps.html", {"attached_maps": attached_maps, "unattached_maps": unattached_maps})

@login_required
def map_view(request, map_id):
    if request.method == "POST":
        if request.POST["submit"] == "Create Component":
            return redirect(f"/racemap/maps/{map_id}/create_component")
        elif request.POST["submit"] == "Rotate Component":
            return redirect(f"/racemap/maps/{map_id}/rotate_component")
        elif request.POST["submit"] == "Delete Component":
            return redirect(f"/racemap/maps/{map_id}/delete_component")
        elif request.POST["submit"] == "Start Game":
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"START_GAME {map_id}\n".encode())
            reply = s.recv(1024).decode()
            s.close()
            messages.success(request, reply)
        elif request.POST["submit"] == "Stop Game":
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"STOP_GAME {map_id}\n".encode())
            reply = s.recv(1024).decode()
            s.close()
            messages.success(request, reply)
        elif request.POST["submit"] == "Save Game":
            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"SAVE {map_id}\n".encode())
            reply = s.recv(1024).decode()
            s.close()
            messages.success(request, reply)

    _map = User.objects.get(username=request.user).maps.get(id=map_id)
    comps = Component.objects.filter(map=map_id).order_by("x", "y")
    return render(request, "map.html", {"map": _map, "comps": comps})

@login_required
def create_component(request, map_id):
    if request.method == "POST":
        form = ComponentCreateForm(request.POST)
        if form.is_valid():
            comp_type = form.cleaned_data["comp_type"]
            x = form.cleaned_data["x"]
            y = form.cleaned_data["y"]

            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"CREATE_COMP {map_id} {comp_type} {x} {y}\n".encode())
            reply = s.recv(1024).decode()
            s.close()

            if "is not registered" in reply or "Position out of map bounds." in reply or "There is already a component" in reply:
                messages.error(request, reply)
            else:
                _map = Map.objects.get(id=map_id)
                _type = ComponentRegistry.objects.get(type=comp_type)
                Component.objects.create(map=_map, type=_type, x=x, y=y)
                messages.success(request, reply)
                return redirect(f"/racemap/maps/{map_id}")
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            messages.error(request, error_string)

    return render(request, "create_component.html", {"form": ComponentCreateForm})

@login_required
def rotate_component(request, map_id):
    if request.method == "POST":
        form = ComponentRotateDeleteForm(request.POST)
        if form.is_valid():
            x = form.cleaned_data["x"]
            y = form.cleaned_data["y"]

            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"ROTATE_COMP {map_id} {x} {y}\n".encode())
            reply = s.recv(1024).decode()
            s.close()

            if "Position out of map bounds." in reply or "There is no component at position" in reply:
                messages.error(request, reply)
            else:
                _map = Map.objects.get(id=map_id)
                comp = Component.objects.get(map=_map, x=x, y=y)
                comp.rotation = (comp.rotation + 1) % 4
                comp.save()
                messages.success(request, reply)
                return redirect(f"/racemap/maps/{map_id}")
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            messages.error(request, error_string)

    return render(request, "rotate_component.html", {"form": ComponentRotateDeleteForm})

@login_required
def delete_component(request, map_id):
    if request.method == "POST":
        form = ComponentRotateDeleteForm(request.POST)
        if form.is_valid():
            x = form.cleaned_data["x"]
            y = form.cleaned_data["y"]

            s = socket(AF_INET, SOCK_STREAM)
            s.connect(("127.0.0.1", 8001))
            s.send(f"USER {request.user}\n".encode())
            s.recv(1024)
            s.send(f"DELETE_COMP {map_id} {x} {y}\n".encode())
            reply = s.recv(1024).decode()
            s.close()

            if "Component deleted." not in reply:
                messages.error(request, reply)
            else:
                _map = Map.objects.get(id=map_id)
                Component.objects.get(map=_map, x=x, y=y).delete()
                messages.success(request, reply)
                return redirect(f"/racemap/maps/{map_id}")
        else:
            error_string = ' '.join([' '.join(x for x in l) for l in list(form.errors.values())])
            messages.error(request, error_string)

    return render(request, "delete_component.html", {"form": ComponentRotateDeleteForm})
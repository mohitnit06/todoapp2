from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == '' or request.POST['username'] == '':
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Username/ Pasword can not be empty. Please Try Again'})
        elif request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'UserName Already Taken. Please Try Again'})
            except ValueError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Please add UserName. Please Try Again'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords Mismatch. Please Try Again.'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Wrong Input. Please Try Again.'})
        else:
            login(request, user)
            return redirect('currenttodos')

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, completed_date__isnull=True).order_by('-created_date')
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, completed_date__isnull=False).order_by('-completed_date')
    return render(request, 'todo/completedtodos.html', {'todos':todos})

@login_required
def viewtodo(request, todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == 'GET':

        form = TodoForm(instance=todo)
        return render(request, 'todo/detail.html', {'todo':todo, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/detail.html', {'todo':todo, 'form':form,'error':'Input params invalid. Please try again.'})

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            todo_created = form.save(commit=False)
            todo_created.user = request.user
            todo_created.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(),'error':'Input params invalid. Please try again.'})

@login_required
def completetodo(request, todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == 'POST':
        todo.completed_date = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo=get_object_or_404(Todo, pk=todo_pk, user = request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

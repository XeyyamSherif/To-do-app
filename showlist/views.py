from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.models import  auth
from django.contrib.auth import authenticate, login
from .models import TodoItem
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required(login_url='/signin/')
def Home(request):
    all_todo_items = TodoItem.objects.filter(author=request.user)

    return render(request, 'home.html',
                  {
                      'all_items':  all_todo_items
                  })

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(username=username, password=password)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/signin/')
    return HttpResponseRedirect('/')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/signin/')

def add_user(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User.objects.create_user(username=username, first_name=first_name,
    last_name=last_name,password=password)

    return HttpResponseRedirect('/')


@csrf_exempt
def adTodo(request):
    c = request.POST['content']
    new_item = TodoItem(content=c, author=request.user)
    new_item.save()
    return HttpResponseRedirect('/')


@csrf_exempt
def deleteTodo(request, todo_id):
    item_id = TodoItem.objects.get(id=todo_id)
    TodoItem.objects.filter(id=todo_id).delete()
    return HttpResponseRedirect('/')




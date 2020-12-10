from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.models import  auth
from django.contrib.auth import authenticate, login
from .models import TodoItem
from django.utils import timezone
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.core import serializers

@login_required(login_url='/signin/')
def Home(request):
    return render(request, 'home.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')

def login(request):
    if request.user.is_authenticated:
        print(request.user)
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




#           AJAX CODES


def get_data(request):

    items = TodoItem.objects.filter(author=request.user).order_by('-added_time')
    data = serializers.serialize('json', list(items))   
    data1 = json.loads(data)
    
    return JsonResponse(data1,safe=False)


@csrf_exempt
def delete_to_do(request):
    to_do_item = request.POST.get('id')
    TodoItem.objects.get(id=to_do_item).delete()
    return HttpResponse('')


@csrf_exempt
def edit_todo(request):
    to_do_item = request.POST.get('id')
    edited_content = request.POST.get('edited_content')
    edited_todo = TodoItem.objects.get(id=to_do_item)
    edited_todo.content = edited_content
    edited_todo.save()
    return HttpResponse('')

def add_new_todo(request):
    new_todo = request.POST.get('to_do_item')
    new_todo_item = TodoItem(content=new_todo, author=request.user).save()
    return HttpResponse('')
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import *
from django.http import JsonResponse

# Create your views here.
@login_required(login_url='/login/')
def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists() and username != request.user.username:
            return redirect('chat_app', username)
        else:
            if username == request.user.username:
                messages.error(request, "User not allowed to text to himself!")
            else:
                messages.error(request, "User With that username doesn't exists")
            return redirect('/')
    friends = {}
    for friend in request.user.user.all():
        friends[friend.friend] = []
        for message in friend.friend.sender.filter(sender=User.objects.filter(username=friend.friend).first(), receiver = request.user):
            if(message.read == False ):
                friends[message.sender].append(message)
    return render(request, 'chat/index.html', {'friends':friends.items()})

@login_required(login_url='/login/')
def chat_app(request, username):
    friend = User.objects.filter(username=username).first()
    if not friend:
        return redirect('/')
    if request.method == 'POST':
        text = request.POST['text']
        if text:
            Message.objects.create(sender=request.user, receiver=friend, text=text)
            return redirect('chat_app', username)
    user_messages = list(Message.objects.filter(sender=request.user, receiver=friend))
    friend_messages = list(Message.objects.filter(sender=friend, receiver=request.user))
    for message in friend_messages:
        message.read = True
        message.save()
    in_messages = user_messages + friend_messages
    for i in range(len(in_messages)):
        pos = i
        for j in range(i+1, len(in_messages)):
            if in_messages[pos].id < in_messages[j].id:
                pos = j
        temp = in_messages[i]
        in_messages[i] = in_messages[pos]
        in_messages[pos] = temp
    return render(request, 'chat/chat_app.html', {'friend': friend, 'in_messages': in_messages})

@login_required(login_url="/login/")
def get_messages(request, username):
    friend = User.objects.get(username=username)
    friend_messages = list(Message.objects.filter(sender=friend, receiver=request.user))
    unread_messages = []
    for message in friend_messages:
        if message.read != True:
            unread_messages.append(message.text)
            message.read = True
            message.save()
    return JsonResponse({'unread_messages': unread_messages})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        elif password != confirm_password:
            messages.error(request, "Passwords dosen't match!")
            return redirect('register')
        user = User.objects.create(username=username)
        user.set_password(password)
        user.save()
        login(request, user)
        return redirect('/')
    return render(request, 'chat/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        messages.error(request, "Invalid Username/password")
        return redirect('login')
    return render(request, 'chat/login.html')

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('login')
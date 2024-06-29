from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .models import Profile, FriendRequest, Message
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, MessageForm
from itertools import chain
from .utils import search


def home(request):
    if request.user.is_authenticated:
        unread_messages = Message.objects.filter(receiver = request.user.profile, seen = False)
        count = unread_messages.count()
        context={'count':count, 'unread_messages':unread_messages}
    else:
        context={}
    return render(request, 'home.html', context)

def loginUser(request):

    page = "login"

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            print("Username doesn't exist")
            messages.error(request, "Username doesn't exist")

        user = authenticate(request, username=username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            print("Password is incorrect")
            messages.error(request, "Password is incorrect")

    context = {"page":page}
    return render(request, 'login-register.html', context)

def registerUser(request):
    form = LoginForm()

    if request.method == 'POST':
        # user = User.objects.create(
        #     username = request.POST['username'],
        #     password = request.POST['password'],   Nu merge pentru ca nu avem detalii despre id si created
        #     email = request.POST['email']
        # )
        form = LoginForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.username = user.username.lower() 
            user.save()
            login(request, user)
            return redirect('home')

    page = 'register'
    context = {'form':form, 'page':page}
    return render(request, 'login-register.html', context)

def logoutUser(request):
  
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def friendsUser(request):
    profile = request.user.profile
    friends = profile.friends.all()
    context = {'friends':friends}
    return render(request, 'friends.html', context)

@login_required(login_url='login')
def removeFriend(request, pk):
    friendProfile = Profile.objects.get(id = pk)
    profile = request.user.profile
   
    profile.friends.remove(friendProfile)
    
    return redirect('friends')

@login_required(login_url='login')    
def searchPeople(request):
    search_query, profiles = search(request)
    friendRequests = FriendRequest.objects.filter(sender=request.user.profile)
    context = {'profiles':profiles, 'friendRequests':friendRequests, 'search_query':search_query}
    return render(request, 'search-people.html', context)

@login_required(login_url='login')
def addFriend(request, pk):
    myProfile = request.user.profile
    friendProfile = Profile.objects.get(id = pk)
    myProfile.friends.add(friendProfile)
    friendRequest = FriendRequest.objects.filter(receiver = myProfile, sender = friendProfile)
    friendRequest.delete()
    return redirect('friend-requests')

@login_required(login_url='login')
def sendFriendRequest(request, pk):
    try:
        myProfile = request.user.profile
        friendProfile = Profile.objects.get(id=pk)
        friendRequest = FriendRequest.objects.create(sender = myProfile, receiver = friendProfile)
        return redirect('searchPeople')
    except IntegrityError:
        print('Deja ai trimis o cerere de prietenie')
        return redirect('searchPeople')

@login_required(login_url='login')
def friendRequests(request):
    profile = request.user.profile
    friend_requests= FriendRequest.objects.filter(receiver = profile)
    context = {'friend_requests':friend_requests}
    return render(request, 'friend-request.html', context)

@login_required(login_url='login')
def removeRequest(request, pk):
    friend_request= FriendRequest.objects.get(id=pk)
    friend_request.delete()
    return redirect('friend-requests')

@login_required(login_url='login')
def show_messages(request, pk):
    friend = Profile.objects.get(id=pk)
    given_messages = Message.objects.filter(receiver = request.user.profile, sender = friend)
    sent_messages = Message.objects.filter(receiver = friend, sender = request.user.profile)
    all_messages = list(chain(given_messages, sent_messages))

    all_messages_sorted = sorted(all_messages, key=lambda x: x.created)
    for message in given_messages:
        message.seen = True
        message.save()
    context = {'messages':all_messages_sorted, 'friend':friend}
    return render(request, 'messages.html', context)

@login_required(login_url='login')
def sendMessage(request, pk):

    friendProfile = Profile.objects.get(id = pk)
    context = {'friend':friendProfile}
    if request.method == 'POST':
        message = Message(request.POST)
        message.body = request.POST['message']
        message.sender = request.user.profile
        message.receiver = friendProfile
        message.save()
        return redirect('message', friendProfile.id)

@login_required(login_url='login')
def notifications(request):
    if request.user.is_authenticated:
        unread_messages = Message.objects.filter(receiver = request.user.profile, seen = False)
        count = unread_messages.count()
        context = {'unread_messages':unread_messages, 'count':count}
    else:
        context={}
    return render(request, 'notifications.html', context)

@login_required(login_url='login')
def myProfile(request):
    if request.user.is_authenticated:
        profile = request.user.profile
    else:
        redirect('login')
    
    context = {'profile':profile}
    return render(request, 'my_profile.html', context)


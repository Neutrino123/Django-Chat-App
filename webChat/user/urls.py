from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('friends/', views.friendsUser, name='friends'),
    path('friends/delete/<str:pk>/', views.removeFriend, name='remove-friend'),
    path('friends/add/<str:pk>/', views.addFriend, name='add-friend'),
    path('search/', views.searchPeople, name='searchPeople'),
    path('friend-requests/', views.friendRequests, name='friend-requests'),
    path('send-friend-request/<str:pk>/', views.sendFriendRequest, name='send-friend-request'),
    path('remove-request/<str:pk>', views.removeRequest, name='remove-request'),
    path('send-message/<str:pk>/', views.sendMessage, name='send-message'),
    path('message/<str:pk>/', views.show_messages, name='message'),
    path('notifications/', views.notifications, name = 'notifications'),
    path('my-profile/', views.myProfile, name ='my-profile'),
]
from .models import Profile, Message
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password', 'password2']
        labels ={'first_name':'Name'}

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
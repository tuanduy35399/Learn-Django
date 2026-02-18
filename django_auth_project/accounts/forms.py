from django.contrib.auth.forms import UserChangeForm,UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= CustomUser
        fields= UserCreationForm.Meta.fields + ("name","bio", "phone_number")

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        models = CustomUser
        fields = UserChangeForm.Meta.fields 

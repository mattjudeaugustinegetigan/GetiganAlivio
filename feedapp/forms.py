from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Pet 
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm


class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet  
        fields = ['name', 'age', 'breed', 'food_preference', 'feeding_schedule']  

class UserProfileForm(UserChangeForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'email')

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']  # Allow editing of username and email only
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter new email'}),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
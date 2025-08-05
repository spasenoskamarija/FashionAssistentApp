# assistant/forms.py
from django import forms
from .models import Profile, ClothingItem, UserOutfit
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserOutfit

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'gender']  # <-- add gender

class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = ['image']

class UserOutfitForm(forms.ModelForm):
    class Meta:
        model = UserOutfit
        fields = ['image', 'rating', 'favorite']



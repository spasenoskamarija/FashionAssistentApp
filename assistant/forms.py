# assistant/forms.py
from django import forms
from .models import Profile, ClothingItem, UserOutfit, OutfitPlan
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
        fields = ['profile_picture', 'gender']

class ClothingItemForm(forms.ModelForm):
    class Meta:
        model = ClothingItem
        fields = ['image']

class UserOutfitForm(forms.ModelForm):
    class Meta:
        model = UserOutfit
        fields = ['image', 'rating', 'favorite']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }


class OutfitPlanForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = OutfitPlan
        fields = ['outfit', 'date', 'note']




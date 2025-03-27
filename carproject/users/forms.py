from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class RegistrationForm(UserCreationForm):
    personal_number = forms.CharField(max_length=20, required=True, label="Personal Number")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'birth_date', 'profile_image']
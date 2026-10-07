from django import forms
from HeartSync.models import *
class UserMF(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose username'
            }),

            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Create password'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
        }

class ProfileMF(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['username','joined_at','is_active']
        
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={
                'class': 'form-control-file'
            }),

            'firstname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'First name'
            }),

            'lastname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Last name'
            }),

            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),

            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your age'
            }),

            'profession': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Software Developer'
            }),

            'city': forms.Select(attrs={
                'class': 'form-control'
            }),

            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us something about yourself...'
            }),

            'interests': forms.CheckboxSelectMultiple(),
        }
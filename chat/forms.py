from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Offer

# Create your forms here.
class NewUserForm(UserCreationForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'first name',
        })
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'last name',
        })
    )

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Username',
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Email',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Password',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control bg-dark text-white',
            'placeholder': 'Confirm Password',
        })
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class OfferForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
    }))
    description = forms.Textarea()
    price = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 
    }))

    class Meta:
        model = Offer
        fields = ("title", "description", "price")
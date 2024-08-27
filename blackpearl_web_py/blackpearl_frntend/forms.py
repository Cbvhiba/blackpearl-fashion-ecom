from .models import *
from django import forms
from django.contrib.auth import authenticate
from django.db.models import Q

class CustomSignupForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )

    class Meta:
        model = CustomerUser
        fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        email = cleaned_data.get('email')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")

        if email and CustomerUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f"Email '{email}' is already in use.")
        
        return cleaned_data



class CustomSigninForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        error_messages={'required': 'Email is required'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        error_messages={'required': 'Password is required'}
    )

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            try:
                user = CustomerUser.objects.get(email=email)
                if not user.check_password(password):
                    raise ValidationError('Invalid email or password')
            except CustomerUser.DoesNotExist:
                raise ValidationError('Invalid email or password')

        return cleaned_data

        
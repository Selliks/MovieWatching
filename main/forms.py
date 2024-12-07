from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")

        return password_confirm

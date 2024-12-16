from django import forms
from django.contrib.auth.models import User
from .models import Movie, Genre


class MovieForm(forms.ModelForm):
    release_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
    )

    class Meta:
        model = Movie
        fields = ['title', 'description', 'age', 'genre', 'author', 'release_date', 'preview_image', 'video_file']

    genre = forms.ModelChoiceField(queryset=Genre.objects.all(), empty_label="Choose genre")


class ChangeUserStatusForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username')
    status = forms.ChoiceField(choices=[('user', 'User'), ('author', 'Author')], label='Status')


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        label='Username',
        error_messages={'required': 'This field is required'}
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='Password',
        error_messages={'required': 'This field is required'}
    )


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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

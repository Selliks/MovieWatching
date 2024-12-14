from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, MovieForm
from django.shortcuts import render, redirect
from decorators import author_required, admin_required
from .models import Author


def main(request):
    if request.user.is_authenticated:
        return redirect('showcase')
    return render(request, 'main.html')


@login_required
def profile(request):
    return render(request, "profile.html")


@author_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('showcase')
    else:
        form = MovieForm()

    return render(request, 'profile.html', {'form': form})


@login_required
def showcase(request):
    return render(request, "showcase.html")


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('showcase')
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'register/login.html', {'form': form})


def registration_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('showcase')
        else:
            print(f"Form errors: {form.errors}")
    else:
        form = RegisterForm()

    return render(request, 'register/registration.html', {'form': form})

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, MovieForm
from django.shortcuts import render, redirect
from .decorators import admin_required, author_required
from .models import Genre, Movie


def main(request):
    if request.user.is_authenticated:
        return redirect('showcase')
    return render(request, 'main.html')


@login_required
def profile(request):
    return render(request, "profile/profile.html")


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('main')
    return render(request, 'register/logout.html')


@author_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('showcase')
    else:
        form = MovieForm()

    return render(request, 'profile/profile.html', {'form': form})


@login_required
def genre_view(request):
    genres = Genre.objects.all()
    return render(request, "body/genre.html", {'genres': genres})


@login_required
def get_movies_by_genre(request):
    if request.is_ajax() and request.method == "GET":
        genre_id = request.GET.get('genre_id')
        movies = Movie.objects.filter(genre_id=genre_id)
        movie_list = [{"id": movie.id, "title": movie.title} for movie in movies]
        return JsonResponse({"movies": movie_list})


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

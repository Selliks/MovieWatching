from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, MovieForm
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import admin_required, staff_required
from .models import Genre, Movie

User = get_user_model()


def main(request):
    if request.user.is_authenticated:
        return redirect('showcase')
    return render(request, 'main.html')


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def showcase(request):
    genres = Genre.objects.all()
    movies = Movie.objects.all()
    return render(request, "showcase.html", {'genres': genres, 'videos': movies})


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('main')
    return render(request, 'logout.html')


@staff_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('showcase')
    else:
        form = MovieForm()
    genres = Genre.objects.all()
    return render(request, 'profile/add_movie.html', {'form': form, 'genres': genres})


@login_required
def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    return render(request, 'movie_detail.html', {'movie': movie})


''' FUNCTION OF THE GENRES '''


@login_required
def genre_view(request):
    genres = Genre.objects.all()
    return render(request, "genre.html", {'genres': genres})


@login_required
def get_movies_by_genre(request):
    if request.is_ajax() and request.method == "GET":
        genre_id = request.GET.get('genre_id')
        movies = Movie.objects.filter(genre_id=genre_id)
        movie_list = [{"id": movie.id, "title": movie.title} for movie in movies]
        return JsonResponse({"videos": movie_list})


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

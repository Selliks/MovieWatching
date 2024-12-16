from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, MovieForm, ChangeUserStatusForm
from django.shortcuts import render, redirect
from .decorators import admin_required, author_required
from .models import Genre, Movie, Role


def main(request):
    if request.user.is_authenticated:
        return redirect('showcase')
    return render(request, 'main.html')


@login_required
def profile(request):
    return render(request, "profile.html")


@login_required
def showcase(request):
    return render(request, "showcase.html")


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('main')
    return render(request, 'logout.html')


User = get_user_model()


@author_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.author = form.cleaned_data['author']
            movie.save()
            return redirect('showcase')
    else:
        form = MovieForm()

    genres = Genre.objects.all()
    return render(request, 'profile/add_movie.html', {'form': form, 'genres': genres})


@admin_required
def change_permission_view(request):
    if request.method == 'POST':
        form = ChangeUserStatusForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            status = form.cleaned_data['status']
            try:
                user = User.objects.get(username=username)
                if status == 'author':
                    user.roles.add(Role.objects.get(name='author'))
                else:
                    user.roles.remove(Role.objects.get(name='author'))

                user.save()
                messages.success(request, f"Permissions for {username} have been updated to {status}.")
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
            except Role.DoesNotExist:
                messages.error(request, "Role does not exist.")
        else:
            messages.error(request, "Invalid input.")
    else:
        form = ChangeUserStatusForm()

    return render(request, 'profile/change_permission.html', {'form': form})


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
        return JsonResponse({"movies": movie_list})


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

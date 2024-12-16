from django.urls import path
from .views import (main, showcase, login_view, registration_view, profile, add_movie, logout_view,
                    genre_view, get_movies_by_genre, change_permission_view)

urlpatterns = [
    path('', main, name='main'),
    path('showcase/', showcase, name='showcase'),
    path('login/', login_view, name='register/login'),
    path('registration/', registration_view, name='register/registration'),
    path('profile/', profile, name='profile'),
    path('profile/add-movie/', add_movie, name='profile/add_movie'),
    path('logout/', logout_view, name='logout'),
    path('genre/', genre_view, name='genre'),
    path('get_movies/', get_movies_by_genre, name='get_movies_by_genre'),
    path('profile/change-permission/', change_permission_view, name='change_permission'),
]

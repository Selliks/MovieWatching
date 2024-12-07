from django.urls import path
from .views import main, showcase, login_view

urlpatterns = [
    path('', main, name='main'),
    path('showcase/', showcase, name='showcase'),
    path('login/', login_view, name='register/login')
]
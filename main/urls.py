from django.urls import path
from .views import main, showcase, login_view, registration_view

urlpatterns = [
    path('', main, name='main'),
    path('showcase/', showcase, name='showcase'),
    path('login/', login_view, name='login'),
    path('registration/', registration_view, name='registration')
]

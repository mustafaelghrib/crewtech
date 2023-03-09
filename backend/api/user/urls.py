from django.urls import path

from .views import *

urlpatterns = [
    path('users', UsersAPI.as_view()),
    path('users/<str:user_id>', UserAPI.as_view()),
]

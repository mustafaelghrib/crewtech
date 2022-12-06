from django.urls import path

from ..views.user_views import *

urlpatterns = [
    path('', UsersAPI.as_view()),
    path('<str:action>', UsersAPI.as_view()),
    path('<str:user_id>', UsersAPI.as_view()),
]

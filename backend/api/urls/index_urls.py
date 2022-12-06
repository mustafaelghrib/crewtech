from django.urls import path
from ..views.index_views import index_view

urlpatterns = [
    path('', index_view),
]

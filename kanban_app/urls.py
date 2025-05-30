from django.db import models
from django.urls import path
from .views import BoardListView, BoardCreateView, BoardDetailView, TasksAssignedToMeView, TaskCreateView

urlpatterns = [
    path("boards/", BoardCreateView.as_view()),
    path("boards/", BoardListView.as_view()),
    path("boards/<int:board_id>/", BoardDetailView.as_view()),
    path("tasks/", TasksAssignedToMeView.as_view()),
    path("tasks/create/", TaskCreateView.as_view()),
]

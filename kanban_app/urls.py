from django.db import models
from django.urls import path
from .views import BoardListView, BoardCreateView, BoardDetailView, TasksAssignedToMeView, TaskCreateView, TaskReviewView, TaskEditView, TaskDeleteView, TaskCommentView, TaskCreateCommentView, TaskDeleteCommentView

urlpatterns = [
    path("boards/", BoardCreateView.as_view()),
    path("boards/", BoardListView.as_view()),
    path("boards/<int:board_id>/", BoardDetailView.as_view()),
    path("tasks/", TasksAssignedToMeView.as_view()),
    path("tasks/create/", TaskCreateView.as_view()),
    path("tasks/<int:task_id>/review/", TaskReviewView.as_view()),
    path("tasks/<int:task_id>/edit/", TaskEditView.as_view()),
    path("tasks/<int:task_id>/delete/", TaskDeleteView.as_view()),
    path("tasks/<int:task_id>/comments/", TaskCommentView.as_view()),
    path("tasks/<int:task_id>/comments/create/", TaskCreateCommentView.as_view()),
    path("tasks/<int:task_id>/comments/<int:comment_id>/delete/", TaskDeleteCommentView.as_view()),
]

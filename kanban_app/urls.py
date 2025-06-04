from django.db import models
from django.urls import path
from .views import BoardListView, BoardCreateView, BoardDetailView, TasksAssignedToMeView, TaskCreateView, TaskReviewView, TaskDetailView, TaskCommentView, TaskDeleteCommentView

urlpatterns = [
    path("boards/", BoardCreateView.as_view()),
    path("boards/", BoardListView.as_view()),
    path("boards/<int:board_id>/", BoardDetailView.as_view()),
    path("tasks/assigned-to-me/", TasksAssignedToMeView.as_view()),
    path("tasks/reviewing/", TaskReviewView.as_view()),
    path("tasks/", TaskCreateView.as_view()),
    path("tasks/<int:task_id>/", TaskDetailView.as_view()),
    path("tasks/<int:task_id>/comments/", TaskCommentView.as_view()),
    path("tasks/<int:task_id>/comments/<int:comment_id>/", TaskDeleteCommentView.as_view()),
]

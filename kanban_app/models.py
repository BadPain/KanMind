from django.db import models
from django.conf import settings


class Board(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_boards'
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='boards'
    )


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    assignee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_tasks'
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    due_date = models.DateField(null=True, blank=True)
    priority = models.CharField(
        max_length=20,
        choices=[
            ("low", "Low"),
            ("medium", "Medium"),
            ("high", "High")
        ]
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("to-do", "To Do"),
            ("in-progress", "In Progress"),
            ("done", "Done"),
            ("review", "Review")
        ]
    )


class Comment(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

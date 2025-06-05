from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Board, Task
from .serializers import BoardOverviewSerializer, BoardSerializer, TaskSerializer, CommentSerializer
from kanban_app.models import Board


User = get_user_model()


class BoardListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        boards = Board.objects.filter(
            models.Q(owner=user) | models.Q(members=user)
        ).distinct()

        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

    def post(self, request):
        title = request.data.get("title")
        member_ids = request.data.get("members", [])

        if not title:
            return Response({"error": "Title is required."}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        board = Board.objects.create(title=title, owner=user)

        if isinstance(member_ids, list):
            members = User.objects.filter(
                id__in=member_ids).exclude(id=user.id)
            board.members.set(members)

        serializer = BoardSerializer(board)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class BoardDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        if request.user != board.owner:
            return Response({"detail": "You do not have permission to edit this board."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BoardSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            updated_board = serializer.save()
            return Response(BoardOverviewSerializer(updated_board).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        if request.user != board.owner:
            return Response({"detail": "You do not have permission to edit this board."}, status=status.HTTP_403_FORBIDDEN)

        serializer = BoardSerializer(board, data=request.data, partial=True)
        if serializer.is_valid():
            updated_board = serializer.save()
            return Response(BoardOverviewSerializer(updated_board).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, board_id):
        board = get_object_or_404(Board, id=board_id)
        if request.user != board.owner:
            return Response({"detail": "You do not have permission to delete this board."}, status=status.HTTP_403_FORBIDDEN)
        board.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TasksAssignedToMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(assignee=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save(assignee=request.user)
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(reviewer=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if request.user != task.assignee:
            return Response({"detail": "You do not have permission to edit this task."}, status=status.HTTP_403_FORBIDDEN)

        serializer = TaskSerializer(
            task, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_task = serializer.save()
            response_serializer = TaskSerializer(
                updated_task, context={'request': request})
            return Response(response_serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        if request.user != task.assignee:
            return Response({"detail": "You do not have permission to delete this task."}, status=status.HTTP_403_FORBIDDEN)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TaskCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        comments = task.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, task_id):
        task = get_object_or_404(Task, id=task_id)
        comment_text = request.data.get("content")

        if not comment_text:
            return Response({"detail": "Comment text is required."}, status=status.HTTP_400_BAD_REQUEST)

        comment = task.comments.create(
            author=request.user, content=comment_text)

        return Response({
            "id": comment.id,
            "created_at": comment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "author": comment.author.first_name,
            "content": comment.content
        }, status=status.HTTP_201_CREATED)


class TaskDeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, task_id, comment_id):
        task = get_object_or_404(Task, id=task_id)
        comment = task.comments.filter(id=comment_id).first()

        if not comment:
            return Response({"detail": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user != comment.author:
            return Response({"detail": "You do not have permission to delete this comment."}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

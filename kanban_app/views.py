from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Board, Task
from .serializers import BoardOverviewSerializer, BoardSerializer, TaskSerializer
from kanban_app.models import Board


User = get_user_model()


class BoardListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        boards = Board.objects.filter(
            models.Q(owner=user) | models.Q(members=user)).distinct()
        serializer = BoardOverviewSerializer(boards, many=True)
        return Response(serializer.data)

class BoardCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        title = request.data.get("title")
        members = request.data.get("members", [])
        user = request.user

        board = Board.objects.create(title=title, owner=user)
        board.members.set(User.objects.filter(id__in=members))

        return Response({
            "id": board.id,
            "title": board.title,
            "member_count": board.members.count(),
            "ticket_count": board.tasks.count(),
            "tasks_to_do_count": board.tasks.filter(status="to-do").count(),
            "tasks_high_prio_count": board.tasks.filter(priority="high").count(),
            "owner_id": board.owner.id
        }, status=status.HTTP_201_CREATED)

class BoardDetailView(APIView):
    permission_classes = [IsAuthenticated]

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

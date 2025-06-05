from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Board, Task, Comment

User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class BoardOverviewSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source='owner.id')
    owner_data = UserMiniSerializer(source="owner", read_only=True)
    members = UserMiniSerializer("members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id", "title",
            "owner_id", "owner_data", "members"
        ]


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_id",
        ]


class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    owner_data = UserMiniSerializer(source="owner", read_only=True)
    members = UserMiniSerializer("members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members"]


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserMiniSerializer(read_only=True)
    reviewer = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "board",
            "title",
            "description",
            "status",
            "priority",
            "assignee",
            "reviewer",
            "due_date",
            "comments_count"
        ]

    def get_reviewer(self, obj):
        if obj.reviewer is None:
            return []
        return [UserMiniSerializer(obj.reviewer).data]

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

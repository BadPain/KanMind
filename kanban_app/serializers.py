from rest_framework import serializers
from .models import Board, Task, Comment, User
from django.contrib.auth import get_user_model
User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class BoardOverviewSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()
    owner_id = serializers.IntegerField(source='owner.id')
    owner_data = UserMiniSerializer(source="owner", read_only=True)
    members_data = UserMiniSerializer(
        source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id", "title",
            "member_count", "ticket_count",
            "tasks_to_do_count", "tasks_high_prio_count",
            "owner_id", "owner_data", "members_data"
        ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status='to-do').count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority='high').count()


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'title', 'owner', 'members']

    def create(self, validated_data):
        members_data = validated_data.pop('members', [])
        board = Board.objects.create(**validated_data)
        board.members.set(members_data)
        return board

    def update(self, instance, validated_data):
        members_data = validated_data.pop('members', None)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        if members_data is not None:
            instance.members.set(members_data)
        return instance


class TaskSerializer(serializers.ModelSerializer):
    assignee = UserMiniSerializer(read_only=True)
    reviewer = UserMiniSerializer(read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id", "board", "title", "description", "status", "priority",
            "assignee", "reviewer", "due_date", "comments_count"
        ]

    def get_comments_count(self, obj):
        return obj.comments.count()


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

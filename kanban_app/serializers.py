from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Board, Task, Comment

User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(source="first_name")

    class Meta:
        model = User
        fields = ["id", "email", "fullname"]


class BoardSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "owner_id",
        ]


class BoardPostSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source="owner.id", read_only=True)
    member_count = serializers.SerializerMethodField()
    ticket_count = serializers.SerializerMethodField()
    tasks_to_do_count = serializers.SerializerMethodField()
    tasks_high_prio_count = serializers.SerializerMethodField()

    class Meta:
        model = Board
        fields = [
            "id",
            "title",
            "member_count",
            "ticket_count",
            "tasks_to_do_count",
            "tasks_high_prio_count",
            "owner_id",
        ]

    def get_member_count(self, obj):
        return obj.members.count()

    def get_ticket_count(self, obj):
        return obj.tasks.count()

    def get_tasks_to_do_count(self, obj):
        return obj.tasks.filter(status="to-do").count()

    def get_tasks_high_prio_count(self, obj):
        return obj.tasks.filter(priority="high").count()


class BoardUpdateResponseSerializer(serializers.ModelSerializer):
    owner_data = UserMiniSerializer(source="owner", read_only=True)
    members_data = UserMiniSerializer(
        source="members", many=True, read_only=True)

    class Meta:
        model = Board
        fields = ["id", "title", "owner_data", "members_data"]


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
            return {}
        return [UserMiniSerializer(obj.reviewer).data]

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskCreateSerializer(serializers.ModelSerializer):
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
        reviewer = obj.reviewer or (obj.board.owner if obj.board else None)
        if reviewer is None:
            return None
        return UserMiniSerializer(reviewer).data

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskBoardSerializer(serializers.ModelSerializer):
    assignee = UserMiniSerializer(read_only=True)
    reviewer = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
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
            return {}
        return [UserMiniSerializer(obj.reviewer).data]

    def get_comments_count(self, obj):
        return obj.comments.count()


class TaskPatchSerializer(serializers.ModelSerializer):
    assignee = UserMiniSerializer(read_only=True)
    reviewer = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    reviewer_id = serializers.PrimaryKeyRelatedField(
        source="reviewer",
        queryset=User.objects.all(),
        write_only=True
    )

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
            "reviewer_id",
            "due_date",
            "comments_count"
        ]

    def get_reviewer(self, obj):
        if obj.reviewer is None:
            return None
        return UserMiniSerializer(obj.reviewer).data

    def get_comments_count(self, obj):
        return obj.comments.count()


class BoardOverviewSerializer(serializers.ModelSerializer):
    owner_id = serializers.IntegerField(source='owner.id')
    members = UserMiniSerializer("members", many=True, read_only=True)
    tasks = TaskBoardSerializer("tasks", many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id", "title",
            "owner_id",
            "members",
            "tasks"
        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']

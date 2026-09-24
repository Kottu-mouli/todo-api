from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import Todo
from .serializers import (
    TodoListSerializer,
    TodoSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "register":
            return UserRegistrationSerializer
        return UserSerializer

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[AllowAny],
        url_path="register",
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            UserSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        return Response(UserSerializer(request.user).data)


class TodoViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Todo.objects
            .filter(user=self.request.user)
            .select_related("user")
        )

    def get_serializer_class(self):
        if self.action == "list":
            return TodoListSerializer
        return TodoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        todo = self.get_object()
        todo.status = Todo.Status.COMPLETED
        todo.save(update_fields=["status", "updated_at"])
        return Response(TodoSerializer(todo).data)

    @action(detail=True, methods=["post"])
    def reopen(self, request, pk=None):
        todo = self.get_object()
        todo.status = Todo.Status.PENDING
        todo.save(update_fields=["status", "updated_at"])
        return Response(TodoSerializer(todo).data)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        stats = self.get_queryset().aggregate(
            total=Count("id"),
            pending=Count("id", filter=Q(status=Todo.Status.PENDING)),
            in_progress=Count(
                "id",
                filter=Q(status=Todo.Status.IN_PROGRESS),
            ),
            completed=Count("id", filter=Q(status=Todo.Status.COMPLETED)),
        )
        return Response(stats)

    @action(detail=False, methods=["get"], url_path="by-status")
    def by_status(self, request):
        status_value = request.query_params.get("status")

        valid_statuses = {choice[0] for choice in Todo.Status.choices}
        if status_value not in valid_statuses:
            return Response(
                {
                    "detail": (
                        "Invalid status. Use one of: "
                        "pending, in_progress, completed."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = self.get_queryset().filter(status=status_value)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = TodoListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(TodoListSerializer(queryset, many=True).data)

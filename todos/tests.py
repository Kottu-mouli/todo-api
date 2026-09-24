from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Todo

User = get_user_model()


class TodoAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="StrongPass123",
        )
        self.other_user = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="StrongPass123",
        )
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {RefreshToken.for_user(self.user).access_token}"
        )

    def test_user_can_only_see_own_todos(self):
        own = Todo.objects.create(user=self.user, title="Own todo")
        Todo.objects.create(user=self.other_user, title="Other todo")

        response = self.client.get("/api/todos/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], own.id)

    def test_user_cannot_access_other_users_todo(self):
        todo = Todo.objects.create(user=self.other_user, title="Private")

        response = self.client.get(f"/api/todos/{todo.id}/")

        self.assertEqual(response.status_code, 404)

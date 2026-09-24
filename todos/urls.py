from rest_framework.routers import DefaultRouter

from .views import TodoViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("todos", TodoViewSet, basename="todo")

urlpatterns = router.urls

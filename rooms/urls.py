from rest_framework.routers import DefaultRouter
from .views import GroupRoomViewSet

router = DefaultRouter()
router.register(r'group_rooms', GroupRoomViewSet, basename='group_room')

urlpatterns = router.urls

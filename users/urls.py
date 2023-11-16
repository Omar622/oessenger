from rest_framework.routers import SimpleRouter
from .views import UserViews

router = SimpleRouter()
router.register(r'user', UserViews, basename="user")

urlpatterns = router.urls


from rest_framework.routers import DefaultRouter

from vimacon.views import InboxViewSet

router = DefaultRouter()
router.register(r'inbox', InboxViewSet)

urlpatterns = router.urls

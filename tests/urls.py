# Rest Framework
from rest_framework import routers

# This app
from .views import GroupViewSet, ProfileViewSet, UserViewSet


router = routers.SimpleRouter()

router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)
router.register('groups', GroupViewSet)

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter

from downtimes import api_views

router = DefaultRouter()
router.register("tags", api_views.TagViewSet)

urlpatterns = router.urls

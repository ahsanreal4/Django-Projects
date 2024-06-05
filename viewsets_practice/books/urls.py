from rest_framework.routers import DefaultRouter
from .views import BookView

router = DefaultRouter(trailing_slash=False)
router.register('books', BookView, basename='books')

urlpatterns = router.urls
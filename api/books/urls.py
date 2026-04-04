from django.urls import include, path
from rest_framework import routers

from api.books.views import BookViewSet

router = routers.DefaultRouter()
# router.register(r"books", include("api.books.urls"))  # 包含 books 应用的 URL
router.register(
    r"", BookViewSet, basename="book"
)  # 包含 books 应用的 URL。这是ViewSet自动路由


urlpatterns = [
    path("", include(router.urls)),  # 包含 DRF 自动生成的 URL
]

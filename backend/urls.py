"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

# Swagger
from rest_framework import permissions, routers

from api.views import HelloWorldView, LoginView, UserViewSet

schema_view = get_schema_view(
    openapi.Info(
        title="DRF + React API",
        default_version="v1",
        description="API documentation for my project",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


router = routers.DefaultRouter()
router.register(r"", UserViewSet)

urlpatterns = [
    path("users/", include(router.urls)),  # 包含 DRF 自动生成的 URL
    path("admin/", admin.site.urls),
    # 添加 HelloWorldView 的 URL
    # 直接通过 name 获取 URL
    # url = reverse("hello-world")  # → /api/hello/
    path("api/hello/", HelloWorldView.as_view(), name="hello-world"),
    path("api/login/", LoginView.as_view(), name="login"),
    # 包含 books 应用的 URL
    path("books/", include("api.books.urls")),  # 包含 books 应用的
    # Swagger 文档
    path(
        "docs/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

# +++++++++++++++++++++++++++++++++++++++++++++++
# 新增：开发环境下允许访问 media 文件（头像、上传文件）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# +++++++++++++++++++++++++++++++++++++++++++++++

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
from rest_framework import routers

from api.views import HelloWorldView, UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),  # 包含 DRF 自动生成的 URL
    path("admin/", admin.site.urls),
    # 添加 HelloWorldView 的 URL
    # 直接通过 name 获取 URL
    # url = reverse("hello-world")  # → /api/hello/
    path("api/hello/", HelloWorldView.as_view(), name="hello-world"),
]

# +++++++++++++++++++++++++++++++++++++++++++++++
# 新增：开发环境下允许访问 media 文件（头像、上传文件）
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# +++++++++++++++++++++++++++++++++++++++++++++++

from django.contrib.auth.models import User
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})


# ---------------------- 用户管理
# ModelSerializer
# {
#   "id": 1,
#   "title": "Rust 编程",
#   "author": 1,      // 关联数据 → 用 ID
#   "category": 2     // 关联数据 → 用 ID
# }
# HyperlinkedModelSerializer 带超链接的ModelSerializer
# {
#   "id": 1,
#   "title": "Rust 编程",
#   "author": "http://localhost:8000/api/authors/1/",   // 超链接
#   "category": "http://localhost:8000/api/categories/2/" // 超链接
# }
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name"]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

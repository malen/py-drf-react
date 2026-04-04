from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, serializers, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import UserProfile
from api.pagination import CustomPagination


# Create your views here.
class HelloWorldView(APIView):
    def get(self, request):
        return Response({"message": "Hello, World!"})


# ---------------------- 用户管理
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["homepage", "avatar"]


class UserListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = [
            "url",
            "id",
            "username",
            "email",
        ]


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
    # 因为模型中 UserProfile 是通过 OneToOneField 关联到 User 的，所以在 UserSerializer 中添加一个 profile 字段，使用 UserProfileSerializer 来序列化它。
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = [
            "url",  # HyperlinkedModelSerializer 默认会添加一个 url 字段，指向该对象的详情页
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "profile",
        ]

    def create(self, validated_data):
        # 因为字段叫 profile，所以 pop("profile")
        profile_data = validated_data.pop("profile", {})
        user = User.objects.create(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})
        instance.username = validated_data.get("username", instance.username)
        instance.email = validated_data.get("email", instance.email)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.save()

        profile = instance.userprofile
        profile.homepage = profile_data.get("homepage", profile.homepage)
        profile.avatar = profile_data.get("avatar", profile.avatar)
        profile.save()

        return instance


# ModelViewSet 自带 6 个接口，包括：
# list（列表）
# retrieve（详情）✅ 自动实现
# create（创建）
# update（更新）
# delete（删除）
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination  # 分页类，使用全局默认分页设置

    # 过滤 + 搜索 + 排序
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["username", "email"]  # 过滤字段
    search_fields = ["username", "email", "first_name", "last_name"]  # 搜索字段
    ordering_fields = ["username", "email"]  # 排序字段

    def get_serializer_class(self):
        if self.action in ["list"]:
            return UserListSerializer
        return UserSerializer

    def get_queryset(self):
        user = self.request.user
        # 管理圆看全部，普通用户只看自己
        if user.is_staff:
            return User.objects.all().order_by("id")
        return User.objects.filter(id=user.id)


# 图书的视图在 books/views.py 中实现，避免 api/views.py 过于臃肿
# 如何创建books/views.py？直接在 api 目录下创建一个 books 目录，在 books 目录下创建一个 views.py 文件即可。
# Serializer 也放在 books 目录下，创建一个 serializers.py 文件。


# JWT 登录接口
class LoginView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # 调用父类的 post 方法，获取 JWT token
        response = super().post(request, *args, **kwargs)
        # 获取用户信息
        user = User.objects.get(username=request.data.get("username"))
        user_data = UserSerializer(user, context={"request": request}).data
        # 将用户信息添加到响应中
        response.data["user"] = user_data
        return response

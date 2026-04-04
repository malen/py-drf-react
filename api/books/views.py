from rest_framework import permissions, viewsets

from api.books.models import Book
from api.books.Serializers import BookSerializer


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    自定义权限类：只有书籍的创建者才能修改或删除书籍，其他用户只能查看书籍列表和详情。
    """

    def has_object_permission(self, request, view, obj):
        # 任何人都可以查看书籍列表和详情
        if request.method in permissions.SAFE_METHODS:
            return True
        # 只有创建者才能修改或删除书籍
        return obj.creator == request.user


class BookViewSet(viewsets.ModelViewSet):
    """图书 CRUD 全套接口
    list（列表）
    retrieve（详情）✅ 自动实现
    create（创建）
    update（更新）
    partial_update（部分更新）
    delete（删除）
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [
        # permissions.AllowAny
    ]  # 可以个别指定权限。需要先登录（http://127.0.0.1:8000/admin/）才能创建、修改、删除 书籍，其他用户只能查看书籍列表和详情

    # 重写方法。这里可以添加权限控制，例如只有登录用户才能创建、修改、删除书籍，其他用户只能查看书籍列表和详情
    def get_permissions(self):
        if self.action in ["create", "list", "retrieve"]:
            self.permission_classes = [
                permissions.IsAuthenticated
            ]  # 需要登录才能创建、浏览 书籍
        elif self.action in ["update", "partial_update", "destroy"]:
            self.permission_classes = [
                IsCreatorOrReadOnly
            ]  # 需要登录才能修改、删除 书籍
        return super().get_permissions()

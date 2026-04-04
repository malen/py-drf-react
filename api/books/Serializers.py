from rest_framework import serializers

from api.books.models import Book


class BookSerializer(serializers.ModelSerializer):
    # ModelSerializer 会自动根据模型字段生成对应的序列化字段
    class Meta:
        model = Book
        fields = "__all__"  # 也可以指定具体的字段，如 fields = ["id", "title", "author", "category"]
        read_only_fields = ["creator", "created_at", "updated_at"]  # 只读字段，不能修改

    def create(self, validated_data):
        # 在创建书籍时，自动将当前用户设置为 creator
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["creator"] = request.user
        return super().create(validated_data)

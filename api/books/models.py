from django.contrib.auth.models import User
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=100, verbose_name="书名")
    author = models.CharField(max_length=100, verbose_name="作者")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="价格")
    category = models.CharField(max_length=100, verbose_name="分类")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    # 创建者（用于权限：智能修改自己的书)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="books",
        null=True,
        blank=True,
        verbose_name="创建者",
    )

    def __str__(self):
        return self.title

    # Meta 类用于定义模型的元数据，例如数据库表名、排序方式等
    class Meta:
        verbose_name = "书籍"  # 单数形式
        verbose_name_plural = "书籍"  # 复数形式
        ordering = ["-created_at"]  # 默认按照创建时间倒序排列

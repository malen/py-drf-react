# Create your models here.

from django.contrib.auth.models import User
from django.db import models


# 扩展User模型 添加 homepage 和 avatar
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    homepage = models.URLField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True)  # 需要安装 Pillow 库

    def __str__(self):
        return self.user.username

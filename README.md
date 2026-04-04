# py-drf-react

Django Rest Framework + React 的示例

## 创建项目

```bash
uv init
uv add django djangorestframework==3.17.1
# 创建 Django 项目
uv run django-admin startproject backend .
# 创建 API 应用
uv run python manage.py startapp api
```
# 运行项目
```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

# 扩展User 模型，添加homepage和avatar字段到UserProfile 中
```py
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    homepage = models.URLField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True)  # 需要安装 Pillow 库

    def __str__(self):
        return self.user.username
```
## 添加了新的模型，需要重新migrate
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```
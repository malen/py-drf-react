# py-drf-react

Django Rest Framework + React 的示例

# 创建项目
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

# 功能增强

## 配置权限
需要先通过http://127.0.0.1:8000/admin/ 登录之后，才能访问被保护的api。

## 添加依赖
uv add djangorestframework-simplejwt django-filter drf-yasg


# TIPS：DRF中的视图
1. ViewSet系列
  1.1 ModelViewSet（自动拥有6个接口）
  1.2 ReadOnlyModelViewSet (只读接口，非常常用，只有两个接口：list 和retrieve)
  1.3 ViewSet（最基础，需要自己实现接口）

2. GenericAPIView 系列
  像搭积木一样，自己拼出需要的接口
    ListModelMixin → list（列表）
    RetrieveModelMixin → retrieve（详情）
    CreateModelMixin → create（创建）
    UpdateModelMixin → update（全量更新）
    PartialUpdateModelMixin → partial_update（部分更新）
    DestroyModelMixin → destroy（删除）
  ```py
    from rest_framework import viewsets, mixins

    class UserViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
  ```

3. APIView 系列（最原始，最自由。适合写非标准接口，比如登录，上传，导出，自定义逻辑）
    各种现成通用视图
    ListAPIView → 列表
    RetrieveAPIView → 详情
    CreateAPIView → 创建
    UpdateAPIView → 更新
    DestroyAPIView → 删除
    ListCreateAPIView → 列表 + 创建
    RetrieveUpdateAPIView → 详情 + 更新
    RetrieveDestroyAPIView → 详情 + 删除
    RetrieveUpdateDestroyAPIView → 详情 + 更新 + 删除

## 最精简总结
ModelViewSet = 全功能王者，全部6个接口
ReadOnlyModelViewSet = 只读专用
APIView = 自由万能，自己写
GenericAPIView + Mixin = 灵活拼装，自己选择


## 用DRF自带的功能，可跨数据库导出，导入
# 如果主键都是uuid（自然键），而不是数字自增ID的话，不需要--natural-foreign --natural-primary
uv run python manage.py dumpdata --natural-foreign --natural-primary -o backup.json
uv run python manage.py loaddata backup.json
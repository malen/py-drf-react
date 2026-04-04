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
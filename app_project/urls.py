"""app_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from app_api.views.category import CategoryView
from app_api.views.comment import CommentView
from app_api.views import TagView, ReactionView, RareUserView, PostView, register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'comments', CommentView, 'comment')
router.register(r'posts', PostView, 'posts')
router.register(r'categories', CategoryView, 'category')
router.register(r'tags', TagView, 'tag')
router.register(r'reactions', ReactionView, 'reaction')
router.register(r'users', RareUserView, 'rareuser')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),

    path('', include(router.urls))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

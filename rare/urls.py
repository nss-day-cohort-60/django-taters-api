"""rare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from rareapi.views import register_user, login_user
from rest_framework import routers
from django.urls import include, path
from rest_framework import routers
from rareapi.views import CategoryView, AuthorView, TagView


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryView, 'category')
router.register(r'tags', TagView, 'tag') #set up url, tell server which view to use when it sees that url, and assign a base name in case of error
router.register(r'authors', AuthorView, 'author')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
]


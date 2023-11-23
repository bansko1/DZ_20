"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from blogapp.api_views import SkillViewSet, WordlViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'skills', SkillViewSet)
router.register(r'words', WordlViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls', namespace='blog')),
    path('users/', include('userapp.urls', namespace='users')),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('api/v0/', include(router.urls)),
    # path('words/', include(router.urls)),
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#
# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns = [
#         path("__debug__/", include("debug_toolbar.urls")),
#     ] + urlpatterns
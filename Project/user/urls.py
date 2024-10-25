from django.contrib import admin
from django.urls import path
from .views import *
from Project import settings
from django.conf.urls.static import static

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name="register"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
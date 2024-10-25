from django.contrib import admin
from django.urls import path
from .views import *
from Project import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', CoreLoginView.as_view(), name="login"),
    path('logout/', CoreLogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
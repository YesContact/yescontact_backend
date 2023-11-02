from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('user/', include('users.urls'), name='user'),
    path('api/', include('users.api.urls'), name='api'),
]

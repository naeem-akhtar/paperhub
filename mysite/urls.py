from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path(r'admin/', admin.site.urls),
  path(r'', include('papers.urls')),
  path(r'', include('posts.urls')),
  path(r'', include('users.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
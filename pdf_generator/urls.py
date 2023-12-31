from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# from pdf_generator.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('users.urls')),
    path('', include('notes.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

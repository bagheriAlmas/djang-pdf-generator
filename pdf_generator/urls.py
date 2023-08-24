from django.contrib import admin
from django.urls import path, include

from pdf_generator.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', home_view, name='home'),
    path('', include('users.urls'))
]

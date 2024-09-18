from django.contrib import admin
from django.urls import path, include  # Asegúrate de importar 'path' y 'include'
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # Incluye las URLs de la aplicación
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Para servir archivos media en desarrollo

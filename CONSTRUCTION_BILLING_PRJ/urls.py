
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include("accounts.urls")),
    path('companies/',include("company.urls")),
    path('projects/',include("project.urls")),
    path('consultants/',include("consultant.urls")),
    path('clients/',include("owner.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
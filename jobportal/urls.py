from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),

    path(
        '',
        TemplateView.as_view(template_name='home.html'),
        name='home'
    ),

    path(
        'accounts/',
        include('useraccounts.urls')
    ),

    path(
    'company/',
    include('companies.urls')

    ),

    path(
    'jobs/',
    include('jobs.urls')
    ),

    path(
    'applications/',
    include('applications.urls')
    ),
    
]
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
 )

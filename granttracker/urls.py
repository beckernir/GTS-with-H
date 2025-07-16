"""
URL configuration for granttracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # Core app URLs
    path('', include('core.urls')),
    
    # App-specific URLs
    path('grants/', include('grants.urls')),
    path('budget/', include('budget.urls')),
    path('reporting/', include(('reporting.urls', 'reporting'), namespace='reporting')),
    path('training/', include('training.urls')),
    path('community/', include('community.urls')),
    path('ai-engine/', include('ai_engine.urls')),
    path('procurement/', include('procurement.urls')),
    
    # API URLs
    path('api/', include('api.urls')),
    
    # Authentication URLs (Django built-in)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Redirect root to dashboard
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='home'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error pages
# handler404 = 'core.views.custom_404'
# handler500 = 'core.views.custom_500'

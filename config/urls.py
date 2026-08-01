"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),

    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
    path('parcelles/', include(('parcelles.urls', 'parcelles'), namespace='parcelles')),
    path('exploitation/', include(('exploitation.urls', 'exploitation'), namespace='exploitation')),
    path('cultures/', include(('cultures.urls', 'cultures'), namespace='cultures')),
    path('recoltes/', include(('cultures.urls', 'cultures'), namespace='recoltes')),
    path('activites/', include(('activites.urls', 'activites'), namespace='activites')),
    path('stock/', include(('stock.urls', 'stock'), namespace='stock')),
    path('ventes/', include(('ventes.urls', 'ventes'), namespace='ventes')),
    path('finances/', include(('finances.urls', 'finances'), namespace='finances')),
    
    path(
        '',
        include(('utilisateurs.urls', 'utilisateurs'), namespace='utilisateurs')
    ),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

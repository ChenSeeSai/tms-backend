"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='TMS API')
urlpatterns = [
    path(
        'admin/', admin.site.urls
    ),
    path(
        'api/doc/', schema_view
    ),
    path(
        'api/',
        include(
            ('tms.account.urls', 'account'),
            namespace='account'
        )
    ),
    path(
        'api/',
        include(
            ('tms.info.urls', 'info'),
            namespace='info'
        )
    ),
    path(
        'api/',
        include(
            ('tms.route.urls', 'route'),
            namespace='route'
        )
    ),
    path(
        'api/',
        include(
            ('tms.vehicle.urls', 'vehicle'),
            namespace='vehicle'
        )
    ),
    path(
        'api/',
        include(
            ('tms.order.urls', 'order'),
            namespace='order'
        )
    ),
    path(
        'api/',
        include(
            ('tms.business.urls', 'business'),
            namespace='business'
        )
    ),
    path(
        'api/',
        include(
            ('tms.security.urls', 'security'),
            namespace='security'
        )
    ),
    path(
        'api/warehouse/',
        include(
            ('tms.warehouse.urls', 'warehouse'),
            namespace='warehouse'
        )
    ),
    path(
        'api/',
        include(
            ('tms.notification.urls', 'notification'),
            namespace='notification'
        )
    ),
    path(
        'api/hr/',
        include(
            ('tms.hr.urls', 'hr'),
            namespace='hr'
        )
    ),
    path(
        'api/finance/',
        include(
            ('tms.finance.urls', 'finance'),
            namespace='finance'
        )
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

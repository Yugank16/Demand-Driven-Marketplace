from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='DEMAND DRIVEN MARKETPLACE API')

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^swagger/$', schema_view),
    url(r'', include('apps.users.urls', namespace='users')),
    url(r'', include('apps.items.urls', namespace='items')),
    url(r'', include('apps.bids.urls', namespace='bids')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

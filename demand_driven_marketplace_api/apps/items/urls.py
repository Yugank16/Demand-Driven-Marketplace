from django.conf.urls import include, url

from rest_framework.authtoken import views

from apps.items.views import ItemViewSet

urlpatterns = [
    url(r'api/items/$', ItemViewSet.as_view({
        'get': 'list',
    }), name='items')
]



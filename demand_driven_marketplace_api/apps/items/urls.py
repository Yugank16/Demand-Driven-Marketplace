from django.conf.urls import include, url

from apps.items.views import ItemViewSet

urlpatterns = [
    url(r'^api/items/$', ItemViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='items')
]



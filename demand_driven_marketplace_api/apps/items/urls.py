from django.conf.urls import include, url

from apps.items.views import ItemViewSet

urlpatterns = [
    url(r'^api/requests/$', ItemViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='items')
]


    
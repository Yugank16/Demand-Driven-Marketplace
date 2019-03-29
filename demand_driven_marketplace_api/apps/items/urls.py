from django.conf.urls import include, url

from apps.items.views import ItemViewSet, SelfItemRequest

urlpatterns = [
    url(r'^api/requests/$', ItemViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='items'),
    url(r'^api/request-details/(?P<pk>\d+)/$', ItemViewSet.as_view({
        'get': 'retrieve',
    }), name='item-detail'),
    url(r'^api/my-requests/$', SelfItemRequest.as_view({
        'get': 'list',
    }), name='my-requests'),
    url(r'^api/request/delete/(?P<pk>\d+)/$', SelfItemRequest.as_view({
        'delete': 'destroy',
    }), name='request-delete'),

]

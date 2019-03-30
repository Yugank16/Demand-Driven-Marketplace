from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static

from apps.bids.views import BidViewSet, ItemRequestBid, PriceUpdate

urlpatterns = [
    url(r'^api/bid/(?P<pk>\d+)/$', BidViewSet.as_view({
        'get': 'retrieve',   
        'delete': 'destroy',
        'patch': 'partial_update',
    })),
    url(r'^api/requests/(?P<item_pk>\d+)/bid/$', ItemRequestBid.as_view({
        'get': 'list',
        'post': 'create',
    })),
    url(r'^api/requests/(?P<item_pk>\d+)/bid/$', ItemRequestBid.as_view({
        'get': 'list',
        'post': 'create',
    })),
    url(r'^api/requests/(?P<item_pk>\d+)/bid/payment/(?P<pk>\d+)/$', ItemRequestBid.as_view({
        'patch': 'partial_update',
    })),
    url(r'^api/my-bids/$', BidViewSet.as_view({
        'get': 'list',
    })),
    url(r'^api/update-bid/(?P<pk>\d+)/$', PriceUpdate.as_view({
        'patch': 'partial_update',
    })),
] 

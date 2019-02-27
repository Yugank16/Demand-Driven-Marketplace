from django.conf.urls import include, url

from apps.users.views import UserViewSet

urlpatterns = [
    url(r'api/users/$', UserViewSet.as_view({
        'post': 'create',
    })),
]

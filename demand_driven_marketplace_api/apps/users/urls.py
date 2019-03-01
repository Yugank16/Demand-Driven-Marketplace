from django.conf.urls import include, url

from rest_framework.authtoken import views

from apps.users.views import UserViewSet, Logout

urlpatterns = [
    url(r'api/users/$', UserViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
    }), name='users'),
    url(r'api/login/$', views.obtain_auth_token, name='login'),
    url(r'api/logout/$', Logout.as_view(), name='logout')
]



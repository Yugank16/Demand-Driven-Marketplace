from django.conf.urls import include, url

from rest_framework.authtoken import views

from apps.users.views import UserViewSet, Logout

urlpatterns = [
    url(r'api/users/$', UserViewSet.as_view({
        'post': 'create',
    })),
    url(r'api/login/$', views.obtain_auth_token),
    url(r'api/logout/$', Logout.as_view())

]

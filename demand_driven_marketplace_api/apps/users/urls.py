from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static

from rest_framework.authtoken import views

from apps.users.views import *

urlpatterns = [
    url(r'api/users/$', UserViewSet.as_view({
        'get': 'retrieve',
        'post': 'create',
        'patch': 'partial_update',
    }), name='users'),
    url(r'api/users/change-password/$', ChangePassword.as_view({
        'patch': 'partial_update',
    }), name='users'),
    url(r'api/login/$', views.obtain_auth_token, name='login'),
    url(r'api/logout/$', Logout.as_view(), name='logout'),
    url(r'^api/password_reset/$',
        ResetPasswordRequestToken.as_view(), name='password_reset'),
    url(r'^api/password_reset/verify/(?P<pk>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ResetPasswordTokenVerification.as_view(), name='password_reset_token_verification'),
    url(r'^api/password_reset/confirm/(?P<pk>\d+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        ResetPasswordConfirm.as_view(), name='password_reset_confirm')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

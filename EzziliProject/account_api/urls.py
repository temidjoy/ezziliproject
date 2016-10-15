

from django.conf.urls import patterns, url, include
from account_api.views import Login, Logout, UserDetails, PasswordReset, PasswordResetConfirm, \
    PasswordChange, UserCred

urlpatterns = patterns(
    'account_api.views',
    url(r'^$', 'new_account', name='registration'),
    url(r'^new_account','new_account', name='registration'),
    # URLs that do not require a session or valid token
    url(r'^login/$', Login.as_view(), name='rest_login'),
    url(r'^password/reset/$', PasswordReset.as_view(),
        name='rest_password_reset'),
    url(r'^password/reset/confirm/$', PasswordResetConfirm.as_view(),
        name='rest_password_reset_confirm'),
    # URLs that require a user to be logged in with a valid session / token.
    url(r'^logout/$', Logout.as_view(), name='rest_logout'),
    url(r'^user/$', UserDetails.as_view(), name='User-detail'),
    url(r'^user/details$', UserCred.as_view(), name='more-list'),
    url(r'^password/change/$', PasswordChange.as_view(), name='rest_password_change'),
    #url(r'^tasks/(?P<pk>[0-9]+)$', 'task_detail', name='task_detail'),
    url(r'^user/(?P<pk>\d+)/moredetail$', UserCred.as_view(), name='More-list')
)

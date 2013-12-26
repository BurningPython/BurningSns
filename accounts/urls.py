'''
Created on 2013年12月12日

@author: july
'''
from django.conf.urls import patterns,url

from accounts import views

urlpatterns = patterns('',
    url(r'^logout$',views.logout_view,name="logout"),
    url(r'^login$|^$',views.login_view,name="login"),
    url(r'^register$',views.register_view,name="register"),
    url(r'^tw_oauth_confirm/(?P<action>\w+)$', views.tw_oauth_confirm, name="tw_oauth_confirm"),
    url(r'^tw_oauth_request/(?P<action>\w+)$', views.tw_oauth_request, name="tw_oauth_request"),
)

'''
Created on 2013年12月12日

@author: july
'''
from django.conf.urls import patterns, url

from accounts import views

urlpatterns = patterns('',
    url(r'^logout$', views.logout_view, name = "logout"),
    url(r'^login$|^$', views.login_view, name = "login"),
    url(r'^register$', views.register_view, name = "register"),
    url(r'^twoacf$', views.tw_oauth_confirm, name = "tw_oauth_confirm"),
    url(r'^twoarq$', views.tw_oauth_request, name = "tw_oauth_request"),
    url(r'^sw_oauth_confirm$', views.sw_oauth_confirm, name = "sw_oauth_confirm"),
    url(r'^sw_oauth_request$', views.sw_oauth_request, name = "sw_oauth_request"),
    url(r'^oauthmanage$',views.oauth_manage_view, name = 'oauth_manage'),
    url(r'^destroy_oauth/(?P<site>\w+)}',views.destroy_oauth,name= 'destroy_oauth')
)

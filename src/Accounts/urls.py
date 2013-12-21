'''
Created on 2013年12月12日

@author: july
'''
from django.conf.urls import patterns,url

from Accounts import views

urlpatterns = patterns('',
    url(r'^logout$',views.logout_view,name="logout"),
    url(r'^login$|^$',views.login_view,name="login"),
    url(r'^register$',views.register_view,name="register"),
    url(r'^tw_oauthProcess$',views.tw_oauthProcess),
    url(r'^tw_oauthBegin$',views.tw_oauthBegin,name = "tw_oauthBegin"),
)
    
from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BurningSns.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$|^index&', views.index_view, name="index"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('accounts.urls', namespace="account")),
    url(r'^home/', include('website.urls', namespace='home')),
)



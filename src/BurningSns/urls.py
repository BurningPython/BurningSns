from django.conf.urls import patterns, include, url

from django.contrib import admin
from . import views
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'BurningSns.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/',include('Accounts.urls',namespace = "account")),
    url(r'^$|^index',views.index_view,name = "index"),
    url(r'^content',views.content_view,name = "content"),
)

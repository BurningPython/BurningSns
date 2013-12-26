from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(r'^$|^content$', views.content_view, name="content"),
                       url(r'^$|^statuses', views.statuses_view, name="content"),
)

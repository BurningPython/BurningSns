from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
                       url(r'^$|^content$', views.content_view, name="content"),
)

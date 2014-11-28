from django.conf.urls import patterns, url
from django.conf import settings
from adminapp import views

urlpatterns = patterns('adminapp.views',
    url(r'^$', views.index, name='index'),
    url(r'^cmd/(?P<command_id>\w+)/$', views.commands, name='commands'),
    
)

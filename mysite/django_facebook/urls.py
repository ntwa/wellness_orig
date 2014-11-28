from django.conf.urls import patterns, url

from django_facebook import views

urlpatterns = patterns('',
     url(r'^$', views.index, name='index'),
   url(r'^faceboook/example/fishtank/(?P<command_id>\w+)/$', views.fishtank, name='fishtank'),
   url(r'^facebook/example/garden/(?P<command_id>\w+)/$', views.fishtank, name='garden'),

  url(r'^facebook/jsondata/(?P<command_id>\w+)/$', views.dataloader, name='dataloader'),
  url(r'^facebook/dataupdate/(?P<command_id>\w+)/$', views.dataupdate, name='dataupdate'),
  url(r'^pagelogout/', views.pagelogout, name='pagelogout'),     
  url(r'^wellness/facebook/dataupdate/(?P<command_id>\w+)/$', views.dataupdate, name='dataupdate'),

)

from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'umidade/(?P<valor>[0-9]+)/$', views.umidade, name='umidade'),
        )
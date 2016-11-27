from django.conf.urls import patterns, url
from app import views

urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^umidade/(?P<valor>[0-9]+)/$', views.umidade, name='umidade'),
        url(r'^ultima_medida/', views.ultima_medida, name='ultima_medida'),
        url(r'^media_medidas/', views.media_medidas, name='media_medidas'),
        url(r'^status_atuador/', views.status_atuador, name='status_atuador'),
        )
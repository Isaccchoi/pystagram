from django.conf.urls import url
from . import views

app_name = 'photos'

urlpatterns = [
    #url(r'^test/$', views.test),
    url(r'^new/$', views.create_post, name='create'),
    url(r'^delete/(?P<pk>[0-9]+)/$', views.delete_post, name='delete'),
    url(r'^(?P<pk>\d+)/$', views.view_post, name='view'),
    url(r'^$', views.list_posts, name='list'),
    url(r'^comments/(?P<pk>[0-9]+)/$', views.delete_comment, name='delete_comment'),
    url(r'^temp/$', views.temp, name='temp'),
    #url(r'', views.list_posts, name='redirect'),
]

from django.conf.urls import url

from . import views

app_name = 'build2myprint'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logged$', views.logged, name='logged'),
    url(r'^list_shoes$', views.list_shoes, name='list_shoes'),
    url(r'^add_shoe$', views.add_shoe, name='add_shoe'),
    url(r'^edit_shoe/(?P<pk>[0-9]*)$', views.edit_shoe, name='edit_shoe')
]

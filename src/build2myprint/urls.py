from django.conf.urls import url

from . import views

app_name = 'build2myprint'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^logged$', views.logged, name='logged'),
]

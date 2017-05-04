from django.conf.urls import url

from . import views

app_name = 'bill2myprint'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rallonge/$', views.RallongeFacultaireView.as_view(), name='rallonge'),
    #url(r'^logged$', views.logged, name='logged'),
    url(r'^sections/$', views.SectionsView.as_view(), name='sections'),

]

from django.conf.urls import url

from . import views

app_name = 'bill2myprint'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rallonge/$', views.RallongeFacultaireView.as_view(), name='rallonge'),
    url(r'^rallonge2/$', views.RallongeFacultaire2View.as_view(), name='rallonge2'),
    url(r'^etudiants/$', views.StudentsView.as_view(), name='etudiants'),
    url(r'^etudiants/(?P<studid>[A-Z0-9-]+)$', views.StudentDetailView.as_view(), name='etudiant_detail'),
    url(r'^etudiants/total/(?P<studid>[A-Z0-9-]+)$', views.studentTotal, name='etudiant_total'),
    #url(r'^logged$', views.logged, name='logged'),
    url(r'^sections/$', views.SectionsView.as_view(), name='sections'),

]

from django.conf.urls import url
from bill2myprint.views import homepage, faculties, sections, students, sciper_list, \
    faculty_extension, status, RallongeFacultaire2View


urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^faculties/$', faculties, name='default_faculties'),
    url(r'^faculties/(?P<faculty>[\w\& ]+)/(?P<semester>[\w\-& ]+)/$', faculties, name='faculties'),
    url(r'^sections/$', sections, name='default_sections'),
    url(r'^sections/(?P<faculty>[\w\& ]+)/(?P<section>[\w\& ]+)/(?P<semester>[\w\-& ]+)/$', sections, name='sections'),
    url(r'^students/$', students, name='default_students'),
    url(r'^students/(?P<sciper>[0-9]+)/$', students, name='students'),
    url(r'^faculty-extension/$', faculty_extension, name='faculty_extension'),
    url(r'^status/$', status, name='status'),
    url(r'^sciper/$', sciper_list),
    # url(r'^rallonge/$', views.RallongeFacultaireView.as_view(), name='rallonge'),
    url(r'^rallonge2/$', RallongeFacultaire2View.as_view(), name='rallonge2'),
    # url(r'^etudiants/$', views.StudentsView.as_view(), name='etudiants'),
    # url(r'^etudiants/(?P<studid>[A-Z0-9-]+)$', views.StudentDetailView.as_view(), name='etudiant_detail'),
    # url(r'^etudiants/total/(?P<studid>[A-Z0-9-]+)$', views.studentTotal, name='etudiant_total'),
    # url(r'^logged$', views.logged, name='logged'),
    # url(r'^sections/$', views.SectionsView.as_view(), name='sections'),
    # url(r'^detail/$', views.detail, name='detail'),
]

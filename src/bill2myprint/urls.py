"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

from django.conf.urls import url
from bill2myprint.views import homepage, faculties, sections, students, sciper_list, \
    faculty_extension, status, compute, student_billing, download_faculty


urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^compute/$', compute, name='compute_all'),
    url(r'^compute/(?P<semester>[\w\-& ]+)/$', compute, name='compute'),
    url(r'^faculties/$', faculties, name='default_faculties'),
    url(r'^faculties/(?P<faculty>[\w\& ]+)/(?P<semester>[\w\-& ]+)/$', faculties, name='faculties'),
    url(r'^sections/$', sections, name='default_sections'),
    url(r'^sections/(?P<faculty>[\w\& ]+)/(?P<section>[\w\& ]+)/(?P<semester>[\w\-& ]+)/$', sections, name='sections'),
    url(r'^students/$', students, name='default_students'),
    url(r'^students/(?P<sciper>[0-9]+)/$', students, name='students'),
    url(r'^student-billing/$', student_billing, name='student_billing'),
    url(r'^faculty-extension/$', faculty_extension, name='faculty_extension'),
    url(r'^status/$', status, name='status'),
    url(r'^sciper/$', sciper_list),

    url(r'^download_faculty/(?P<faculty>[\w\& ]+)/$', download_faculty, name='download_faculty'),
    url(r'^download_faculty/(?P<faculty>[\w\& ]+)/(?P<semester>[\w\-& ]+)/$',
        download_faculty, name='download_faculty'),
]

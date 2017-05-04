"""django_example URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.shortcuts import render

from django_tequila.urls import urlpatterns as django_tequila_urlpatterns

from django_tequila.admin import TequilaAdminSite
admin.autodiscover()
admin.site.__class__ = TequilaAdminSite

urlpatterns = [
    url(r'^', include('bill2myprint.urls')),
    url(r'^not_allowed/', lambda request: render(request, '403.html')),
    url(r'^admin/', admin.site.urls),
]

urlpatterns += django_tequila_urlpatterns

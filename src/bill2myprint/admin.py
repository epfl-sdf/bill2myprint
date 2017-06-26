"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

from django.contrib import admin

from .models import UpdateStatus, Semester, Section, Faculty


class UpdateStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'update_date', 'status', 'message')
    search_fields = ['id', 'update_date', 'status', 'message']


class SemesterAdmin(admin.ModelAdmin):
    list_display = ('name', 'end_date', 'end_date_official')
    search_fields = ['name', 'end_date', 'end_date_official']


class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'acronym', 'faculty')
    search_fields = ['name', 'acronym']


class FactulyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name', ]


admin.site.register(UpdateStatus, UpdateStatusAdmin)
admin.site.register(Semester, SemesterAdmin)
admin.site.register(Section, SectionAdmin)
admin.site.register(Faculty, FactulyAdmin)

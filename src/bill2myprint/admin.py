"""
    (c) All rights reserved. ECOLE POLYTECHNIQUE FEDERALE DE LAUSANNE, Switzerland, VPSI, 2017
"""

from django.contrib import admin

from .models import UpdateStatus


class UpdateStatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'update_date', 'status', 'message')
    search_fields = ['id', 'update_date', 'status', 'message']

admin.site.register(UpdateStatus, UpdateStatusAdmin)

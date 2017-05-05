import re

from django.db.models import Q
from django.core.management.base import BaseCommand

from equitrac.models import TAllTransactions
from bill2myprint.models import Section, Student


class Command(BaseCommand):
    help = 'Populates the database with sections and the faculties'

    def handle(self, *args, **options):
        students = TAllTransactions.objects.filter(hierarchie2='EPFL ETU').exclude(
            Q(hierarchie3__icontains='audit') | Q(hierarchie3__icontains='EME') | Q(hierarchie3__icontains='EDOC'))
        students = students.values_list('person_sciper').distinct()
        for student in students:
            Student.objects.create(sciper=student[0])

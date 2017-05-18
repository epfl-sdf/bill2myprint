from django.db.models import Q
from django.core.management.base import BaseCommand

from equitrac.models import TAllTransactions
from bill2myprint.models import Student


class Command(BaseCommand):
    help = 'Populates the database with sections and the faculties'

    def handle(self, *args, **options):
        students = TAllTransactions.objects.filter(hierarchie2='EPFL ETU').exclude(
            Q(hierarchie3__icontains='audit') | Q(hierarchie3__icontains='EDOC'))
        students = students.values_list('person_sciper').distinct()
        to_save = []
        for student in students:
            to_save.append(Student(sciper=student[0], username=''))
        Student.objects.bulk_create(to_save)

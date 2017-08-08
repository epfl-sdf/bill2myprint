from django.db.models import Q
from django.core.management.base import BaseCommand

from equitrac.models import TAllTransactions
from bill2myprint.models import Student
from staff.models import VPersonHistory, Personnes


class Command(BaseCommand):
    help = 'Populates the database with sections and the faculties'

    def handle(self, *args, **options):
        students = TAllTransactions.objects.filter(hierarchie2='EPFL ETU').exclude(
            Q(hierarchie3__icontains='audit') | Q(hierarchie3__icontains='EDOC'))
        students = students.values_list('person_sciper').distinct()
        to_save = []
        for student in students:
            username = ''
            sciper = student[0]
            try:
                p = Personnes.objects.get(sciper=sciper)
                username = p.username
                name = p.get_full_name()
            except Personnes.DoesNotExist:
                if len(str(sciper)) > 6:
                    sciper = student[0]
                    sciper = str(sciper)[3:]
                try:
                    p = Personnes.objects.get(sciper=sciper)
                    username = p.username
                except Personnes.DoesNotExist:
                    p = VPersonHistory.objects.get(person_sciper=sciper)
                    username = p.person_username
                    name = p.get_full_name()
            if username is None:
                username = ''
            to_save.append(Student(sciper=student[0], username=username, name=name))
        Student.objects.bulk_create(to_save)

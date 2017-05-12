from django.core.management.base import BaseCommand

from bill2myprint.models import Semester


class Command(BaseCommand):
    help = 'Populates the database with sections and the faculties'

    SEMESTERS = [
        ('Automne 2016-2017', '2017-02-19 00:00:00', '2016-12-23 00:00:00'),
        ('Printemps 2016-2017', '2017-09-18 00:00:00', '2017-06-02 00:00:00'),
        ('Automne 2017-2018', '2018-02-18 00:00:00', '2017-12-22 00:00:00'),
    ]

    def handle(self, *args, **options):

        for sem in self.SEMESTERS:
            Semester.objects.create(name=sem[0], end_date=sem[1], end_date_official=sem[2])

from django.core.management.base import BaseCommand, CommandError

from bill2myprint.models import Semester
from equitrac.models import TSemester


class Command(BaseCommand):
    help = 'Populates the database with sections and the faculties'

    def handle(self, *args, **options):
        equitrac_semesters = TSemester.objects.all().order_by('smst_end_date')

        for eq_semester in equitrac_semesters[1:]:
            Semester.objects.create(name=eq_semester.smst_name, end_date=eq_semester.smst_end_date, end_date_official=eq_semester.smst_end_date_official)

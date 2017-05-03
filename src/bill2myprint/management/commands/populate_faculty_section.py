from django.core.management.base import BaseCommand, CommandError
from bill2myprint.models import Section, Faculty


class Command(BaseCommand):
    help = 'Populates the database with sections and the faculties'

    faculties = [
        'ENAC',
        'I&C',
        'SB',
        'STI',
        'SV',
        'CDH',
        'CDM',
        'CMS',
    ]

    sections = [
        ('Architecture', 'AR', 'ENAC'),
        ('Chimie et génie chimique', 'CGC', 'SB'),
        ('Génie civile', 'GC', 'ENAC'),
        ('Génie électrique et électronique', 'EL', 'STI'),
        ('Génie mécanique', 'GM', 'STI'),
        ('Ingénieurie financière', 'IF', 'CDM'),
        ('Mathématiques', 'MA', 'SB'),
        ('Microtechnique', 'MT', 'STI'),
        ('Physique', 'PH', 'SB'),
        ('Systèmes de communication', 'SC', 'I&C'),
        ('Humanités digitales', 'DH', 'CDH'),
        ("Sciences et ingénieurie de l'environnement", 'SIE', 'ENAC'),
        ("Sciences et technologies du vivant", 'SV', 'SV'),
        ('Informatique', 'IN', 'I&C'),
        ('Management de la technologie', 'MTE', 'CDM'),
        ("Management de la technologie et de l'information", 'MGT', 'CDM'),
        ('Science et génie des matériaux', 'MX', 'STI'),
        ('Cours de mathématiques spéciales', 'CMS', 'CMS'),
    ]

    def handle(self, *args, **options):
        for f in self.faculties:
            Faculty.objects.get_or_create(name=f)
        for name, acronym, faculty in self.sections:
            Section.objects.create(name=name, acronym=acronym, faculty=Faculty.objects.get(name=faculty))

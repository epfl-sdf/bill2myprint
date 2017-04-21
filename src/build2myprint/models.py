from django.db import models


class Shoe(models.Model):
    brand = models.CharField(max_length=255)
    size = models.PositiveIntegerField()

    COLOR_CHOICES = (
        ('noir', ('Noir')),
        ('blanc', ('Blanc')),
        ('rouge', ('Rouge')),
        ('bleu', ('Bleu'))
    )

    TYPE_CHOICES = (
        ('course', ('Course')),
        ('marche', ('Marche')),
        ('ville', ('ville'))
    )

    color = models.CharField(max_length=10, choices=COLOR_CHOICES, default='noir')
    shoe_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='ville')

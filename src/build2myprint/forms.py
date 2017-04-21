from django.forms import ModelForm

from .models import Shoe

class ShoeForm(ModelForm):
    class Meta:
        model = Shoe
        fields = ['brand', 'size', 'color', 'shoe_type']

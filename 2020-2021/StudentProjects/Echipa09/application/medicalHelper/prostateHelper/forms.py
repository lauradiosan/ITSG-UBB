from django import forms

from django import forms
from .models import *


class LoadImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['original']

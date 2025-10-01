from django import forms
from .models import Condominio

class CondominioForm(forms.ModelForm):
    class Meta:
        model = Condominio
        fields = ['nombre', 'ciudad']

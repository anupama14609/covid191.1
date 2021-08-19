from django.core import validators
from django import forms
from django.db.models import fields
from django.forms import widgets
from .models import CovidUpdate

class CovidUpdateForm(forms.ModelForm):

    class Meta:
        model = CovidUpdate
        fields = ['search']
        widgets = {
            'search':forms.TextInput(attrs={'class':'form-control','name':'search',
             'value':''})
        }


  
from .models import Lockers
from django import forms

class LockerForm(forms.ModelForm):
    class Meta:
        model = Lockers
        fields = ('name', 'key', 'status')
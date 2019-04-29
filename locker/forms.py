from .models import Locker
from django import forms

class LockerForm(forms.ModelForm):
    class Meta:
        model = Locker
        fields = ('name', 'key', 'status')
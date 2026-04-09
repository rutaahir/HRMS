from django import borrowings
from .models import Task # તમારું Task મોડલ

class TaskSubmitForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['completion_file', 'completion_note'] # મોડલમાં આ ફિલ્ડ્સ હોવા જોઈએ
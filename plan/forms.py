from django.forms import ModelForm
from django import forms
from tbcore.models import Plan
from django.core.exceptions import ValidationError

class NotesForm(forms.Form):
    note_content = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'name':'notes-detail-page', 'rows':'7', 'cols':'40'}))

    def clean_note_content(self):
        data = self.cleaned_data['note_content']
        if len(data) >500:
            raise ValidationError ('Text should not be longer than 500 characters')
        return data

class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['plan_name']

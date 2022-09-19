from django.forms import ModelForm
from django import forms
from tbcore.models import Notes, Plan


class NotesForm(forms.Form):
    note_content = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'name':'notes-detail-page', 'rows':'7', 'cols':'40'}))


class PlanForm(ModelForm):
    class Meta:
        model = Plan
        fields = ['plan_name']

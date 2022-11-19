from django.forms import ModelForm
from django import forms
from tbcore.models import Plan
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper

class NotesForm(forms.Form):
    note_content = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'name':'notes-detail-page', 'rows':'7', 'cols':'50','placeholder': 'Please describe your teaching idea in a few words for your online course checklist.'}))

    def __init__(self, *args, **kwargs):
        super(NotesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    def clean_note_content(self):
        data = self.cleaned_data['note_content']
        if len(data) >500:
            raise ValidationError ('Text should not be longer than 500 characters')
        return data

class PlanForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(PlanForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


    class Meta:
        model = Plan
        fields = ['plan_name']

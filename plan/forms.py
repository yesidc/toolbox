from django.forms import ModelForm
from tbcore.models import Notes, Plan

class NotesForm (ModelForm):
    class Meta:
        model= Notes
        fields= ['idea_note']
        help_texts = {
            'idea_note': ('Some useful help text.'),
        }

class PlanForm (ModelForm):
    class Meta:
        model= Plan
        fields= ['plan_name']

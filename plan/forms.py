from django.forms import ModelForm
from tbcore.models import Notes

class NotesForm (ModelForm):
    class Meta:
        model= Notes
        fields= ['idea_note']
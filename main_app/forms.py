from django.forms import ModelForm
from .models import Meeting

class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['date', 'location', 'note']
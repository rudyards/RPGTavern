from django.forms import ModelForm
from .models import Meeting, Comment


class MeetingForm(ModelForm):
    class Meta:
        model = Meeting
        fields = ['date', 'location', 'note']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


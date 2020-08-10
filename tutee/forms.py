from django import forms
from users.models import UserProfileInfo
from .models import Question
class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('photo', 'gender')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = [
        'title',
        'desc',
        'remarks',
        'difficulty',
        ]

class QuestionFullForm(QuestionForm): #extending form
    attachments = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta(QuestionForm.Meta):
        fields = QuestionForm.Meta.fields + ['attachments',]
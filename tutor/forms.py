from django import forms
from users.models import UserProfileInfo


class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('photo', 'gender')

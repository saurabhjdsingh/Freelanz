from django import forms
from .models import MyPost


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = MyPost
        fields = ['pic', 'subject', 'message']

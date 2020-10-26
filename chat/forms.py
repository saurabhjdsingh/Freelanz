from django import forms
from .models import ChatFile, DeliverFiles


class ChatFileForm(forms.ModelForm):

    class Meta:
        model = ChatFile
        fields = ["file"]


class DeliverFileForm(forms.ModelForm):

    class Meta:
        model = DeliverFiles
        fields = ["file"]
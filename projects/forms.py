from django import forms
from .models import Project, Bid


class CreateProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ["name", "end_date", "budget", "file", "category", "description"]


class CreateBidForm(forms.ModelForm):

    class Meta:
        model = Bid
        fields = ["budget", "description", "date_time"]
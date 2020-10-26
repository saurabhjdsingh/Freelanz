from django import forms
from django.contrib.auth.models import User
from .models import Profile, UserPhone


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']


class EmailUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']


class PhoneUpdateForm(forms.ModelForm):

    class Meta:
        model = UserPhone
        fields = ['phone']


class OtpForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email']
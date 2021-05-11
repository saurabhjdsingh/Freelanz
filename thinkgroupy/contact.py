from django import forms
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from thinkgroupy import settings
from .settings import RECAPTCHA_SITE_KEY, RECAPTCHA_SECRET_KEY
import requests, json

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control' }))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control' }))
    subject = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control' }))
    message = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control' }))


def contact(request):
    submitted = False
    if request.method == 'POST':
        clientkey=request.POST['g-recaptcha-response']
        capchtaData = {
            'secret':RECAPTCHA_SECRET_KEY,
            'response':clientkey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',data=capchtaData)
        response = json.loads(r.text)
        verify = response['success']
        if verify:
            form = ContactForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                html_content = render_to_string('contact_email.html', {
                    'name': cd['name'],
                    'subject': cd['subject'],
                    'message': cd['message'],
                    'from_email': cd['email']
                })
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives(
                    'Message From Thinkgroupy',
                    text_content,
                    settings.EMAIL_HOST_USER,
                    ['singhjdsaurabh@gmail.com'])
                email.attach_alternative(html_content, "text/html")
                email.send()
                return HttpResponseRedirect('/contact?submitted=True')
        else:
            return render(request, 'index.html')
    else:
        form = ContactForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'contact.html',
                  {'form': form, 'submitted': submitted, 'RECAPTCHA_SITE_KEY': RECAPTCHA_SITE_KEY})

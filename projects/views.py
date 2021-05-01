from .forms import CreateProjectForm, CreateBidForm
from . models import Project, Bid, categories, Order, CompletedOrder, EmailSubscription, EmailRequest
from django.shortcuts import HttpResponseRedirect, render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from dashboard.models import Profile, UserPhone
from payments.models import Payment
from django.utils import timezone
import razorpay
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from django.utils import timezone
from twilio.rest import Client
from decouple import config
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from thinkgroupy import settings
User = get_user_model()
client = razorpay.Client(auth=(config("RAZORPAY_KEY"), config("RAZORPAY_SECRET")))


@login_required
def orders(request):
    if CompletedOrder.objects.filter(user=request.user).exists():
        completedorders = CompletedOrder.objects.filter(user=request.user)
    else:
        completedorders = "no"
    if Order.objects.filter(worker=request.user).exists():
        orders = Order.objects.filter(worker=request.user)
    else:
        orders = "no"
    return render(request, 'projects/orders.html', {"orders": orders, "completed": completedorders})


@login_required
def category(request):
    category = categories.objects.all()
    return render(request, "projects/categories.html", {"categories": category})


@login_required
def Slug_Project(request, slug):
    projects = get_object_or_404(Project, slug=slug)
    if EmailSubscription.objects.filter(profile=request.user.profile).exists():
        email = EmailSubscription.objects.get(profile=request.user.profile)
        if Bid.objects.filter(project=projects, created_by=request.user).exists():
            bids = Bid.objects.filter(project=projects, created_by=request.user)
            return render(request, "projects/project_detail.html", {"project": get_object_or_404(Project, slug=slug), 'email': email,"applied": bids})
        return render(request, "projects/project_detail.html", {"project": get_object_or_404(Project, slug=slug),'email': email})
    else:
        if Bid.objects.filter(project=projects, created_by=request.user).exists():
            bids = Bid.objects.filter(project=projects, created_by=request.user)
            return render(request, "projects/project_detail.html", {"project": get_object_or_404(Project, slug=slug), "applied": bids})
        else:
            return render(request, "projects/project_detail.html", {"project": get_object_or_404(Project, slug=slug)})


@login_required
def Category_Project(request, category):
    user = request.user
    cat = get_object_or_404(categories, name=category)
    messages = Project.objects.filter(category=cat.id, completed=False)
    return render(request, "projects/cat_projects.html", {"user": user, "projects": messages, "category": cat})


@login_required
def CreateProject(request):
    profile = Profile.objects.get(user__id=request.user.id)
    user = request.user
    if request.method == 'POST':
        form = CreateProjectForm(request.POST, request.FILES)
        if form.is_valid():
            if request.FILES:
                obj = Project(name=form.cleaned_data['name'], budget=form.cleaned_data['budget'], created_by=user, end_date=form.cleaned_data['end_date'], category=form.cleaned_data['category'], description=form.cleaned_data['description'], file=request.FILES['file'])
            else:
                obj = Project(name=form.cleaned_data['name'], budget=form.cleaned_data['budget'], created_by=user, end_date=form.cleaned_data['end_date'], category=form.cleaned_data['category'], description=form.cleaned_data['description'])
            obj.save()
            request_project = Project.objects.get(name=obj.name)
            html_content = render_to_string('emails/projects/project_live.html', {'project': request_project})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives('Project Live', text_content, settings.EMAIL_HOST_USER, [request.user.email])
            email.attach_alternative(html_content, "text/html")
            email.send()
        return HttpResponseRedirect("/projects/")
    else:
        if profile.completed is True and UserPhone.objects.filter(user=request.user).exists():
            form = CreateProjectForm()
            category = categories.objects.all()
            return render(request, "projects/project_new.html", {'user': user, 'categories': category}) 
        else:
            return redirect('/editprofile')


@login_required
def Projects(request):
    messages = Project.objects.filter(completed=False)
    return render(request, "projects/projects.html", {'projects': messages})


@login_required
def BidProject(request, project):
    user = request.user
    if request.method == 'POST':
        form = CreateBidForm(request.POST)
        if form.is_valid():
            obj = Bid(project=Project.objects.get(slug=project), budget=form.cleaned_data['budget'], created_by=user, date_time=form.cleaned_data['date_time'], description=form.cleaned_data['description'])
            obj.save()
            html_content = render_to_string('emails/projects/application_recieved.html', {'user': request.user, 'message': form.cleaned_data['description']})
            text_content = strip_tags(html_content)
            email = EmailMultiAlternatives('Applicantion recieved for your project', text_content, settings.EMAIL_HOST_USER, [Project.objects.get(slug=project).created_by.email])
            email.attach_alternative(html_content, "text/html")
            email.send()
            return redirect("/projects/")
        return redirect("/projects/")
    else:
        profile = Profile.objects.get(user__id=request.user.id)
        if UserPhone.objects.filter(user=request.user).exists() and profile.completed is True:
            form = CreateBidForm()
            return render(request, "projects/bid.html", {'user': user, 'project': get_object_or_404(Project, slug=project)}) 
        return redirect("/editprofile")


@login_required
def Myprojects(request):
    projects = Project.objects.filter(created_by=request.user)
    if EmailSubscription.objects.filter(profile=request.user.profile).exists():
        email = EmailSubscription.objects.get(profile=request.user.profile)
        if request.method == "POST":
            project_name = request.POST.get("slug")
            request_project = Project.objects.get(name=project_name)
            emails = []
            users = User.objects.all()
            for user in users:
                email = user.email
                emails.append(email)
            e = EmailSubscription.objects.get(profile=request.user.profile)
            if e.email_type == "small":
                email_list = emails[:100]
                number_of_emails = int(100)
            if e.email_type == "medium":
                email_list = emails[:250]
                number_of_emails = int(250)
            if e.email_type == "large":
                email_list = emails[:450]
                number_of_emails = int(450)
            for to_email in email_list:
                email_to = to_email
                user1 = User.objects.get(email=email_to)
                html_content = render_to_string('emails/projects/send_project.html', {'user': user1.username, 'project': request_project})
                text_content = strip_tags(html_content)
                email = EmailMultiAlternatives('Project Invitation', text_content, settings.EMAIL_HOST_USER, [email_to])
                email.attach_alternative(html_content, "text/html")
                email.send()
            e.number_of_emails = int(e.number_of_emails - 1 )
            e.no_of_emails_send = int(e.no_of_emails_send + 1)
            e.save()
            t = EmailRequest(profile=request.user.profile, number_of_emails= number_of_emails, completed=True, expiry_date= timezone.now() + timedelta(1))
            t.save()
            account_sid = config('account_sid')
            auth_token = config('auth_token')
            number = request.user.userphone.phone
            client = Client(account_sid, auth_token)
            messages = "Hey! We have processed your email request and also we have send your project details to our users through mail."
            client.messages.create(
                              body=messages,
                              from_='+18444458559',
                              to=str(number)
                          )
            return redirect("dashboard:dashboard")
        else:
            return render(request, "projects/myprojects.html", {'projects': projects, 'email': email})
    else:
        return render(request, "projects/myprojects.html", {'projects': projects})


@login_required
def Applicants(request, project):
    projects = get_object_or_404(Project, slug=project)
    if request.user == projects.created_by:
        bids = Bid.objects.filter(project=projects)
        return render(request, "projects/applicant_bids.html", {'bids': bids, 'projects': projects})
    else:
        return redirect("dashboard:dashboard")

def buy_emails(request):
    if request.method == "POST":
        if request.POST['amount'] == "small":
            amount = float(0.9)
        elif request.POST['amount'] == "medium":
            amount = float(9.9)
        elif request.POST['amount'] == "large":
            amount = float(19.90)
        else:
            amount = int(0)
        payment_id = request.POST.get('razorpay_payment_id')
        payment_amount = amount*100
        pay = client.payment.fetch(payment_id)
        pay_email = pay.get('email')
        pay_contact = pay.get('contact')
        profile = Profile.objects.filter(user=request.user).first()
        if amount == 19.9:
            cost = 1990
            client.payment.capture(payment_id, cost, {"currency": "USD"})
        else:
            client.payment.capture(payment_id, payment_amount, {"currency": "USD"})
        pay = Payment(profile=profile, payment_amount=payment_amount, payment_date=timezone.now(), payment_id=payment_id, email=pay_email, phone_number=pay_contact, captured=pay.get('captured'))
        pay.save()
        if amount == 0.9:
            if EmailSubscription.objects.filter(profile=request.user.profile).exists():
                email = EmailSubscription.objects.get(profile=request.user.profile)
                email.profile = profile
                email.email_type = 'small'
                email.number_of_emails = int(email.number_of_emails + 1)
                email.save()
            else:
                email = EmailSubscription(profile = profile, email_type = 'small', number_of_emails = int(1))
                email.save()
        elif amount == 9.9:
            if EmailSubscription.objects.filter(profile=request.user.profile).exists():
                email = EmailSubscription.objects.get(profile=request.user.profile)
                email.profile = profile
                email.email_type = 'medium'
                email.number_of_emails = int(email.number_of_emails + 5)
                email.save()
            else:
                email = EmailSubscription(profile = profile, email_type = 'medium', number_of_emails = int(5))
                email.save()
        elif amount == 19.9:
            if EmailSubscription.objects.filter(profile=request.user.profile).exists():
                email = EmailSubscription.objects.get(profile=request.user.profile)
                email.profile = profile
                email.email_type = 'large'
                email.number_of_emails = int(email.number_of_emails + 10)
                email.save()
            else:
                email = EmailSubscription(profile = profile, email_type = 'large', number_of_emails = int(10))
                email.save()
        return redirect('projects:my_project')
    return render(request, "projects/buy_emails.html", {"key": config("RAZORPAY_KEY")})

from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from django.db.models import Q
from django.core.mail import EmailMessage
from django.views import generic
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import ProfileUpdateForm, PhoneUpdateForm
from django.contrib.auth import get_user_model
from .models import Profile
from .models import FollowUser, PrimaryEmail, UserPhone
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
from datetime import timedelta
import secrets
from twilio.rest import Client
from chat.models import Notify
from django.views.decorators.csrf import csrf_exempt
import json
from payments.models import VirtualCurrency, AccountDetails, Tempwallet, Refund
from projects.models import CompletedOrder, Order
import base64
import matplotlib
import matplotlib.pyplot as xyz
from io import BytesIO
matplotlib.use('Agg')
UserModel = get_user_model()


@csrf_exempt
def notify(request):
    if request.method == "POST":
        notifications = int(request.POST.get('unread'))
        if notifications <= 0:
            return HttpResponse(json.dumps({"hello": "1"}), content_type="application/json")
        else:
            x = Notify.objects.filter(user=User.objects.get(username=request.POST.get('user')))
            for i in x:
                i.read = True
                i.save()
            return HttpResponse(json.dumps({"hello": "1"}), content_type="application/json")


@login_required
def dashboard(request):
    user = request.user
    if VirtualCurrency.objects.filter(user=request.user).exists():
        pass
    else:
        obj = VirtualCurrency(user=user)
        obj.save()
    if Refund.objects.filter(user=request.user).exists():
        pass
    else:
        obje = Refund(user=user)
        obje.save()
    time = []
    monthly = 0
    yearly = 0
    Jan = 0
    Feb = 0
    Mar = 0
    Apr = 0
    May = 0
    Jun = 0
    Jul = 0
    Aug = 0
    Sep = 0
    Oct = 0
    Nov = 0
    Dec = 0
    if CompletedOrder.objects.filter(user=request.user).exists():
        com = CompletedOrder.objects.filter(user=request.user).count()
        x = CompletedOrder.objects.filter(user=request.user)
        for i in x:
            print(timezone.now().month == i.completed_on.month)
            if timezone.now().month == i.completed_on.month:
                monthly += i.budget
            if timezone.now().year == i.completed_on.year:
                yearly += i.budget
            if i.completed_on.month == 1:
                Jan += i.budget
            elif i.completed_on.month == 2:
                Feb += i.budget
            elif i.completed_on.month == 3:
                Mar += i.budget
            elif i.completed_on.month == 4:
                Apr += i.budget
            elif i.completed_on.month == 5:
                May += i.budget
            elif i.completed_on.month == 6:
                Jun += i.budget
            elif i.completed_on.month == 7:
                Jul += i.budget
            elif i.completed_on.month == 8:
                Aug += i.budget
            elif i.completed_on.month == 9:
                Sep += i.budget
            elif i.completed_on.month == 10:
                Oct += i.budget
            elif i.completed_on.month == 11:
                Nov += i.budget
            elif i.completed_on.month == 12:
                Dec += i.budget
        graph = [Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec]
        months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] 
        img = BytesIO()

        xyz.plot(months, graph)
        xyz.xticks(months, labels)
        xyz.ylabel('Earning(Rs.)')
        xyz.xlabel('Months')
        xyz.savefig(img, format='png')
        xyz.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    else:
        com = 0
    if Order.objects.filter(worker=request.user).exists():
        progress = Order.objects.filter(worker=request.user)
        for prog in progress:
            time.append((prog.bid.project.name, 100/(prog.bid.date_time- prog.created_on).days))
    elif Order.objects.filter(creator=request.user).exists():
        progress = Order.objects.filter(creator=request.user)
        for prog in progress:
            time.append((prog.bid.project.name, 100/(prog.bid.date_time- prog.created_on).days))
    else:
        progress = "no"
        time = "no"
    if "plot_url" not in locals():
        plot_url = "no"
    return render(request, 'dashboard/dashboard.html', {"time": time, "com": com, "monthly": monthly, "yearly": yearly, "plot": plot_url})


def ProfileDetailView(request, pk):
    form = Profile.objects.get(pk=pk)
    user = FollowUser.objects.filter(profile=form, Followed_by=request.user)

    if user:
        is_followed = True
    else:
        is_followed = False
    return render(request, 'dashboard/profile_detail.html', {'form': form, 'is_followed': is_followed})


def follow(req, pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.create(profile=user, Followed_by=req.user.profile.user)
    return redirect('dashboard:profile', pk)


def unfollow(req, pk):
    user = Profile.objects.get(pk=pk)
    FollowUser.objects.filter(profile=user, Followed_by=req.user.profile.user).delete()
    return redirect('dashboard:profile', pk)


class UserListView(LoginRequiredMixin, ListView):
    login_url = "accounts:signin"
    raise_exception = False

    model = Profile
    context_object_name = 'users'
    template_name = 'dashboard/user_list.html'

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si is None:
            si = ""
        profList = Profile.objects.filter(Q(location__icontains = si)|Q(gender__icontains = si)|Q(organization_name__icontains = si)).order_by("-id");
        for p1 in profList:
            p1.followed = False
            ob = FollowUser.objects.filter(profile=p1, Followed_by=self.request.user)
            if ob:
                p1.followed = True
        return profList


@login_required
def EditProfile(request):
    context = {}
    data = Profile.objects.get(user__id=request.user.id)
    context["data"] = data
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        gender = request.POST["gender"]
        organization_name = request.POST["organization"]
        location = request.POST["location"]
        birth_day = request.POST["birth_day"]

        user = User.objects.get(id=request.user.id)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        data.gender = gender
        data.organization_name = organization_name
        data.location = location
        data.birth_day = birth_day
        data.completed = True
        data.save()
        context["status"] = "Changes saved successfully"
    return render(request, 'dashboard/editprofile.html', context)


@login_required
def EditProfilePic(request):
    if request.method == "POST":
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your Picture was successfully updated!')
            return render(request, 'dashboard/editprofile.html')
        else:
            messages.error(request, 'Try again!')
    else:
        return render(request, 'dashboard/editprofile.html')


@login_required
def security(request):
    return render(request, 'dashboard/security.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,
                             'Your password was successfully updated!')
            return render(request, 'dashboard/security.html')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'dashboard/security.html', {
        'form': form
    })


class DeleteUser(LoginRequiredMixin, generic.DeleteView):
    login_url = "/signin/"
    model = User
    template_name = 'dashboard/security.html'
    success_url = reverse_lazy("index")


def email_activated(request):
    return render(request, 'dashboard/email_activated.html')


def email_activated_false(request):
    return render(request, 'dashboard/email_activated_false.html')


@login_required(login_url='signin')
def EmailUpdate(request):
    user = request.user
    if request.method == 'POST':
        email_for_activation = request.POST['email']
        token = secrets.randbits(16)
        mail_subject = 'Confirm your Mail'
        email = EmailMessage(
            mail_subject, f'Hello{user} here is your otp {token}', to=[email_for_activation]
        )
        email.send()
        obj = PrimaryEmail.objects.filter(user=request.user)
        if obj:
            for i in obj:
                i.email = email_for_activation
                i.token = token
                i.created_on = timezone.now()
                i.save()
        else:
            new = PrimaryEmail(user=request.user, email=email_for_activation, token=token)
            new.save()
        messages.error(request, 'Please verify your new email. Check out your email inbox or spam folder.')
        return redirect('dashboard:otp_verify', email2=email_for_activation)
    else:
        return render(request, 'dashboard/security.html')


@login_required
def otp_verify(request, email2):
    primaryemail = get_object_or_404(PrimaryEmail, user=request.user)
    if request.method == "POST":
        code = request.POST['otp']
        if primaryemail.errors < 3 and code == primaryemail.token and timezone.now() - primaryemail.created_on < timedelta(minutes=3):
            User.objects.filter(id=request.user.id).update(email=primaryemail.email)
            return redirect("dashboard:email_activated")
        else:
            return redirect("dashboard:email_activated_false")
    return render(request, 'dashboard/otp.html')


@login_required
def PhoneUpdate(request):
    if request.method == 'POST':
        form = PhoneUpdateForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            token = secrets.randbits(16)
            account_sid = 'AC929d62e1173b1d610a76aa7aa14f9acc'
            auth_token = '840c3797d4ccac0a7c6ec57f6dd2034c'
            client = Client(account_sid, auth_token)
            body_message = 'Hey! Thanks for making an account on thinkgroupy.com , Your O.T.P for phone Verification is: ' + str(token)
            client.messages.create(
                              body=body_message,
                              from_='+18444458559',
                              to=str(phone)
                          )
            obj = UserPhone.objects.filter(user=request.user)
            if obj:
                for i in obj:
                    i.phone = phone
                    i.token = token
                    i.created_on = timezone.now()
                    i.save()
            else:
                new = UserPhone(user=request.user, token=token)
                new.save()
                messages.error(request, 'Please verify with your O.T.P.')
            request.session['phone'] = str(phone)
            return redirect('dashboard:otp_phone_verify', phone=str(phone))
        else:
            form = PhoneUpdateForm()
            return render(request, 'dashboard/security.html', {'form': form})


@login_required
def otp_phone_verify(request, phone):
    primarynumber = get_object_or_404(UserPhone, user=request.user)
    if request.method == "POST":
        code = request.POST['otp']
        if primarynumber.errors < 3 and code == primarynumber.token and timezone.now() - primarynumber.created_on < timedelta(minutes=3):
            x = UserPhone.objects.filter(user=request.user)
            for i in x:
                i.phone = request.session['phone']
                i.verified = True
                i.save()
                request.session.pop('phone')
                messages.success(request, 'Your number is successfully verified.')
            return redirect("dashboard:security")
        else:
            request.session.pop('phone')
            messages.error(request, 'We are unable to verify your account, try again.')
            return redirect("dashboard:email_activated_false")
    return render(request, 'dashboard/otp.html')


@login_required
def billing(request):
    refund = Refund.objects.get(user=request.user)
    if request.method == "POST":
        name = request.POST.get('user_name')
        ifsc = request.POST.get('ifsc')
        accountnumber = request.POST.get('accnumber')
        bank = request.POST.get('bank_name')
        obj = AccountDetails(user=request.user, account_number=int(accountnumber), name=name, bank_name=bank, ifsc_code=ifsc)
        obj.save()
    if VirtualCurrency.objects.filter(user=request.user).exists():
        wallet = VirtualCurrency.objects.get(user=request.user).budget
    else:
        wallet = 0
    if Tempwallet.objects.filter(user=request.user).exists():
        temp = Tempwallet.objects.filter(user=request.user)
    else:
        temp = 0
    if AccountDetails.objects.filter(user=request.user).exists():
        account = AccountDetails.objects.get(user=request.user)
    else:
        account = "no"
    if CompletedOrder.objects.filter(user=request.user).exists():
        completed = CompletedOrder.objects.filter(user=request.user)
        for i in completed:
            temp = Tempwallet.objects.get(user=request.user)
            if temp.budget != 0:
                if timezone.now() - i.completed_on >= timedelta(days=10):
                    price = VirtualCurrency.objects.get(user=request.user).budget
                    VirtualCurrency.objects.filter(user=request.user).update(budget=float(price)+float(temp.budget))
                    temp.budget = 0
                    temp.save()
        if VirtualCurrency.objects.get(user=request.user).budget > 0:
            if AccountDetails.objects.filter(user=request.user).exists():
                if AccountDetails.objects.get(user=request.user).verified is True:
                    withdraw = "yes"
                    verified = "yes"
                    budget = VirtualCurrency.objects.get(user=request.user).budget
                else:
                    withdraw = "no"
                    verified = "no"
            else:
                withdraw = "no"
        else:
            withdraw = "no"
    else:
        withdraw = "no"
    if 'budget' not in locals():
        budget = "no"
    if 'verified' not in locals():
        verified = "no"
    return render(request, 'dashboard/billing.html',
                  {"wallet": wallet,
                   "temp": temp,
                   "account": account,
                   "withdraw": withdraw,
                   "verified": verified,
                   "budget": budget,
                   "refund": refund})

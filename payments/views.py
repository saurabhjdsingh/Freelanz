from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import razorpay
from django.contrib.auth.decorators import login_required
from .models import VirtualCurrency, AccountDetails, Refund
from django.contrib.auth.models import User
from projects.models import Order, Project, Bid
from chat.models import Notify
import requests
from django.contrib import messages
client = razorpay.Client(auth=("rzp_test_HZxFaqOlnavM73", "VzFO4xqTUVAGW3eAuWB524sj"))


@login_required
def payment_status(request):
    if request.method == "POST":
        refund = Refund.objects.get(user=request.user)
        price = int(request.POST.get('price'))
        payedto = User.objects.get(username=request.POST.get('payedto'))
        payment_id = request.POST.get('razorpay_payment_id')
        payment_amount = price*100
        client.payment.capture(payment_id, payment_amount, {"currency": "INR"})
        Creator = Project.objects.get(created_by=request.user, name=request.POST.get('projectname'))
        bid = Bid.objects.get(project=Creator, created_by=payedto)
        obj = Order(bid=bid, creator=request.user, worker=payedto, paid=int(bid.budget))
        obj.save()
        msh = str(request.user.username)+" has hired you for their project."
        objec = Notify(user=payedto, notification=msh)
        objec.save()
        Creator.completed = True
        Creator.save()

        if refund.budget <= price and refund.budget != 0:
            refund.budget = 0
            refund.save()
        return redirect("chat:room", request.POST.get('payedto'))
    return redirect("/")


@login_required
def confirm_payment(request,  slug, name):
    project = get_object_or_404(Project, slug=slug)
    user = get_object_or_404(User, username=name)
    bid = get_object_or_404(Bid, created_by=user, project=project)
    refund = Refund.objects.get(user=request.user)
    if refund.budget == 0:
        amount = bid.budget
    elif refund.budget >= bid.budget+100:
        obj = Order(bid=bid, creator=request.user, worker=bid.created_by, paid=int(bid.budget))
        obj.save()
        msh = str(request.user.username)+" has hired you for their project."
        objec = Notify(user=bid.created_by, notification=msh)
        objec.save()
        project.completed = True
        project.save()
        refund.budget = refund.budget - (bid.budget+100)
        refund.save()
        return redirect("chat:room", bid.created_by.username)
    else:
        amount = bid.budget-refund.budget
    return render(request, 'payments/payment_page.html', {"project": project, "bid": bid, "amount":amount, "refund":refund})


@login_required
def processwithdrawal(request):
    if request.method == "POST":
        account_id = AccountDetails.objects.get(user=request.user).account_id
        amount = int(request.POST.get('amount'))*100
        headers = {
            'content-type': 'application/json',
        }
        data = {"account": account_id, "amount": amount, "currency": "INR"}
        response = requests.post('https://api.razorpay.com/v1/transfers', headers=headers, json=data, auth=('rzp_test_HZxFaqOlnavM73', 'VzFO4xqTUVAGW3eAuWB524sj'))
        VirtualCurrency.objects.filter(user=request.user).update(budget=0)
        messages.success(request, 'We have transferred the money to your account.')
    return render(request, "dashboard/billing.html")




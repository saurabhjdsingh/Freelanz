from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from .models import Message, RoomId, ChatFile, VideoChat, DeliverFiles, Notify
from .forms import ChatFileForm, DeliverFileForm
from dashboard.models import Profile, FollowUser
import hashlib
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from projects.models import Project, Bid, Order, CompletedOrder
from payments.models import VirtualCurrency, Tempwallet, Refund
import razorpay
client = razorpay.Client(auth=("rzp_test_HZxFaqOlnavM73", "VzFO4xqTUVAGW3eAuWB524sj"))


@login_required
def complete(request):
    if request.method == "POST":
        bidder = User.objects.get(username=request.POST.get('bidder'))
        project = Project.objects.get(name=request.POST.get('projectname'))
        obj = CompletedOrder(user=bidder, order=project.name, created_by=request.user)
        obj.save()
        bid = Bid.objects.get(created_by=bidder, project=project)
        temp = Tempwallet(user=bidder, budget=int(bid.budget)*0.882, order=obj)
        temp.save()
        obj.budget = temp.budget
        obj.save()
        x = Order.objects.get(bid=bid)
        filess = DeliverFiles.objects.filter(order=x)
        for files in filess:
            file = ChatFile(name=files.name, file=files.file, FileFrom=files.FileFrom, FileTo=files.FileTo)
            file.save()
        Order.objects.filter(bid=bid).delete()
        project.delete()
        msh = str(request.user.username)+" has marked the project as completed."
        objec = Notify(user=bidder, notification=msh)
        objec.save()
        return redirect("chat:room", request.POST.get('bidder'))


@login_required
def hire(request):
    if request.method == "POST":
        budget = int(request.POST.get('budget'))*100+200
        if not Refund.objects.get(user=request.user).exists():
            Refund(user=request.user).save()
            refund = 0
            amount = budget
        else:
            print(refund)
            refund = Refund.objects.get(user=request.user)
            
            if refund.budget == 0:
                amount = budget
            elif refund.budget >= budget:
                refund.budget = refund.budget - int(request.POST.get('budget'))*100+200
                refund.save()
            else:
                amount = budget- refund.budget
                refund.budget = 0
                refund.save()
        print(refund)
        response = client.order.create(dict(amount=int(amount), currency="INR"))
        order_id = response['id']
        order_status = response['status']
        if order_status == 'created':
            return render(request, 'payments/confirm_add_money.html', {"amount":budget, "amounttodisplay": int(budget)/100, "order_id":order_id, "projectname":request.POST.get('projectname'), "user":request.POST.get('userpayed'), "refund":refund})
        return redirect("chat:room", request.POST.get('bidder'))


@login_required
def edit_bid(request):
    if request.method == "POST":
        budget = request.POST.get('budget')
        end_date = request.POST.get('date')
        project = Project.objects.get(name=request.POST.get('project'))
        if budget is not None:
            Bid.objects.filter(project=project, created_by=request.user).update(budget=budget)
        if end_date is not None:
            Bid.objects.filter(project=project, created_by=request.user).update(date_time=end_date)
        return redirect("chat:room", request.POST.get('user'))


@login_required
def joincall(request):
    if request.method == "POST":
        if VideoChat.objects.filter(user1=request.user, user2=User.objects.get(username=request.POST.get('user'))).exists():
            room = VideoChat.objects.get(user1=request.user, user2=User.objects.get(username=request.POST.get('user'))).room_name
        elif VideoChat.objects.filter(user2=request.user, user1=User.objects.get(username=request.POST.get('user'))).exists():
            room = VideoChat.objects.get(user2=request.user, user1=User.objects.get(username=request.POST.get('user'))).room_name
        else:
            return redirect("chat:room", request.POST.get('user'))
        return render(request, "chat/video.html", {"user1": request.POST.get('user'), "user2": request.user.username, "room": request.POST.get('room')})


@login_required
def video(request):
    if request.method == "POST":
        roomname = "chat_" + str(request.POST.get('room'))
        Msg = str(request.user.username)+" has started a call. "
        room = RoomId.objects.get(room_name=request.POST.get('room'))
        obj = Message(author=request.user, key=room, message=Msg)
        obj.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            roomname,
            {'type': 'call', 'message': Msg, "caller": request.user.username, "calledto": request.POST.get('user')}
        )
        if VideoChat.objects.filter(user1=request.user, user2=User.objects.get(username=request.POST.get('user'))).exists():
            room = VideoChat.objects.get(user1=request.user, user2=User.objects.get(username=request.POST.get('user'))).room_name
        elif VideoChat.objects.filter(user2=request.user, user1=User.objects.get(username=request.POST.get('user'))).exists():
            room = VideoChat.objects.get(user2=request.user, user1=User.objects.get(username=request.POST.get('user'))).room_name
        else:
            objec = VideoChat(user1=request.user, user2=User.objects.get(username=request.POST.get('user')), room_name=request.POST.get('room'))
            objec.save()
        return render(request, "chat/video.html", {"user1": request.POST.get('user'), "user2": request.user.username, "room": request.POST.get('room')})
    return redirect('/')


@login_required
def room(request, username):
    first_user = request.user
    wallet = VirtualCurrency.objects.get(user=first_user).budget
    second_user = User.objects.get(username=username)
    projects = []
    bidforvalidation = []
    edit = []
    if first_user == second_user:
        return redirect("/")
    if not Order.objects.filter(creator=request.user, worker=second_user).exists() and not Order.objects.filter(creator=second_user, worker=first_user).exists():
        if Project.objects.filter(created_by=request.user).exists():
            projectforvalidation = Project.objects.filter(created_by=request.user)
            for i in projectforvalidation:
                if Bid.objects.filter(created_by=second_user, project=i).exists():
                    vali = Bid.objects.get(created_by=second_user, project=i)
                    pro = Project.objects.get(created_by=request.user, bid=vali)
                    tup = (pro.name, pro.description, vali.description, vali.budget, vali.date_time, pro.slug, vali.created_by)
                    projects.append(tup)
                    order = "no"
                    order_files = "no"
 
                else:
                    order = "no"
                    order_files = "no"
                    projectforvalidation = Project.objects.filter(created_by=second_user)
                    for i in projectforvalidation:
                        if Bid.objects.filter(created_by=request.user, project=i).exists():
                            edit = Bid.objects.get(created_by=request.user, project=i)
                            break
        else:
            order = "no"
            order_files = "no"
            projectforvalidation = Project.objects.filter(created_by=second_user)
            for i in projectforvalidation:
                if Bid.objects.filter(created_by=request.user, project=i).exists():
                    vali = Bid.objects.get(created_by=request.user, project=i)
                    tup = (vali.description, vali.budget, vali.date_time, i.name)
                    edit.append(tup)
                    
    else:
        if Order.objects.filter(creator=request.user, worker=second_user).exists():
            order = Order.objects.get(creator=request.user, worker=second_user)
            if DeliverFiles.objects.filter(order=order).exists():
                order_files = DeliverFiles.objects.filter(order=order)
            else:
                order_files = "no"
            if request.user == order.creator and order.paid != order.bid.budget:
                payment = order.bid.budget
        else:
            order = Order.objects.get(creator=second_user, worker=request.user)
            if DeliverFiles.objects.filter(order=order).exists():
                order_files = DeliverFiles.objects.filter(order=order)
            else:
                order_files = "no"
            deliver = "yes"
    token_name = str(first_user.username) + str(second_user.username)
    token = hashlib.sha256(str(token_name).encode('utf-8')).hexdigest()
    form = Profile.objects.get(user=second_user)
    user = FollowUser.objects.filter(profile=form, Followed_by=request.user)

    if request.method == "POST":
        p_form = ChatFileForm(request.POST, request.FILES)
        if p_form.is_valid():
            if request.FILES:
                obj = ChatFile(name=request.FILES['file'].name.split("/")[-1], FileFrom=first_user, FileTo=second_user, file=request.FILES['file'])
                obj.save()
            pass
    if user:
        is_followed = True
    else:
        is_followed = False

    if RoomId.objects.filter(user1=first_user, user2=second_user).exists() or RoomId.objects.filter(user1=second_user, user2=first_user).exists():
        if RoomId.objects.filter(user1=first_user, user2=second_user).exists():
            room = RoomId.objects.get(user1=first_user, user2=second_user)
        else:
            room = RoomId.objects.get(user2=first_user, user1=second_user)
        if request.user != room.user1 and request.user != room.user2:
            return HttpResponseBadRequest()
        messages = []
        x = Message.objects.filter(key=room).order_by('created_on')
        for i in x:
            tup = [i.author.username, i.message]
            messages.append(tup)
        mess = Message.objects.filter(key=room)
        for i in mess:
            if i.author != request.user:
                i.read = True
                i.save()
        if not 'deliver' in locals():
            deliver = "no"
        if len(projects) == 0:
            projects = "no"
        if len(edit) == 0:
            edit = "no"
        if 'payment' in locals():
            return render(request, 'chat/index.html', {"messagesicon": "no", "inboxforchat": [], "unreadforchat": [], 'room_name': room.room_name, "messages": messages, "second_user": second_user, "first_user": first_user, "is_followed": is_followed, "projects": projects, "bid": bidforvalidation, "order": order, "edit":edit, "payment":payment, "currency": wallet, "orderfiles":order_files, 'deliver':deliver})
        return render(request, 'chat/index.html', {"messagesicon": "no", "inboxforchat": [], "unreadforchat": [],
         'room_name': room.room_name, "messages": messages, "second_user": second_user, "first_user": first_user, "is_followed": is_followed, "projects": projects, "bid": bidforvalidation, "order": order, "edit":edit, "orderfiles":order_files, 'deliver':deliver})
    else:
        room = RoomId(user1=first_user, user2=second_user, room_name=token)
        room.save()
        messages = []
        x = Message.objects.filter(key=room).order_by('created_on')
        for i in x:
            tup = [i.author.username, i.message]
            messages.append(tup)
        mess = Message.objects.filter(key=room)
        for i in mess:
            if i.author != request.user:
                i.read = True
                i.save()
        return render(request, 'chat/index.html', {
         'room_name': room.room_name,  "messages": messages, "second_user": second_user, "first_user": first_user, "is_followed": is_followed, "projects": projects
        })
    return render(request, 'index.html')


@login_required
def chatfiles(request, username):
    first_user = request.user
    second_user = User.objects.get(username=username)
    if ChatFile.objects.filter(FileFrom=first_user, FileTo=second_user).exists() or ChatFile.objects.filter(FileFrom=second_user, FileTo=first_user).exists():
        if ChatFile.objects.filter(FileFrom=first_user, FileTo=second_user).exists() and ChatFile.objects.filter(FileFrom=second_user, FileTo=first_user).exists():
            files_1 = ChatFile.objects.filter(FileFrom=first_user, FileTo=second_user)
            files_2 = ChatFile.objects.filter(FileFrom=second_user, FileTo=first_user)
            return render(request, 'chat/files.html', {"files_2": files_2, "files_1": files_1})
        elif ChatFile.objects.filter(FileFrom=first_user, FileTo=second_user).exists():
            files_1 = ChatFile.objects.filter(FileFrom=first_user, FileTo=second_user)
            return render(request, 'chat/files.html', {"files_1": files_1})
        elif ChatFile.objects.filter(FileFrom=second_user, FileTo=first_user).exists():
            files_2 = ChatFile.objects.filter(FileFrom=second_user, FileTo=first_user)
        return render(request, 'chat/files.html', {"files_2": files_2, "second_user": second_user})
    else:
        message = "You both never shared a single file!"
    return render(request, 'chat/files.html', {"message": message}) 


@login_required
def deliver(request):
    if request.method == "POST":
        p_form = DeliverFileForm(request.POST, request.FILES)
        if p_form.is_valid():
            if request.FILES:
                creator = User.objects.get(username=request.POST.get('creator'))
                obj = DeliverFiles(name=request.FILES['file'].name.split("/")[-1],order = Order.objects.get(creator=creator, worker=request.user), FileFrom=request.user, FileTo=creator, file=request.FILES['file'])
                obj.save()
                msh = str(request.user.username)+" has delivered the files"
                objec = Notify(user=creator, notification=msh)
                objec.save()
        return redirect("chat:room", request.POST.get('creator'))


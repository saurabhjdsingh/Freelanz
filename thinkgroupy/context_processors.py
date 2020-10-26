from chat.models import Message, RoomId, Notify

def get_messages(request):
     if not request.user.is_authenticated:
            return {}
     if request.user.is_authenticated:
        inbox = []
        unread = []
        notread = 0
        notifications = []
        if Notify.objects.filter(user=request.user).exists():
            for i in Notify.objects.filter(user=request.user).order_by('-created_at'):
                notifications.append(i)
        inbox1 = RoomId.objects.filter(user1=request.user)
        inbox2 = RoomId.objects.filter(user2=request.user)
        if RoomId.objects.filter(user1=request.user).exists():
            for i in inbox1:
                if Message.objects.filter(key=i).exists():
                    message = Message.objects.filter(key=i).latest('created_on')
                    x = (i.user1.username, i.user2.username, i.room_name, message.message, message.read, i.user1.profile.image.url, i.user2.profile.image.url)
                    inbox.append(x)
        if inbox2:
            for i in inbox2:
                if Message.objects.filter(key=i).exists():
                    message = Message.objects.filter(key=i).latest('created_on')
                    x = (i.user1.username, i.user2.username, i.room_name, message.message, message.read, i.user1.profile.image.url, i.user2.profile.image.url)
                    inbox.append(x)
        for inbo in inbox:
            if inbo[4] is False:
                inbox.remove(inbo)
                unread.append(inbo)
        for i in notifications:
            if i.read == False:
                notread += 1
        
        return {"unreadno":len(unread), "messagesicon":"yes", "inboxforchat":inbox, "unreadforchat":unread, "userforchat":request.user.username, "firstname":request.user.username, "notifications":notifications, "unreadball":notread}

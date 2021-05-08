from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import RoomId, Message, ChatFile, DeliverFiles, Notify


class RoomIdAdmin(ModelAdmin):
    list_display = ["user1", "user2", "room_name"]
    search_fields = ["user1__username", "user2__username", "room_name"]
    list_filter = ["user1", "user2", "room_name"]


admin.site.register(RoomId, RoomIdAdmin)


class MessageAdmin(ModelAdmin):
    list_display = ["author", "key", "created_on"]
    search_fields = ["key__room_name", "author__username"]
    list_filter = ["key", "created_on"]


admin.site.register(Message, MessageAdmin)

class NotifyAdmin(ModelAdmin):
    list_display = ["read", "user"]
    search_fields = ["read", "user__username"]
    list_filter = ["read", "user"]


admin.site.register(Notify, NotifyAdmin)

class ChatFileAdmin(ModelAdmin):
    list_display = ["FileFrom", "FileTo"]
    search_fields = ["FileFrom__username", "FileTo__username"]
    list_filter = ["FileFrom", "FileTo"]


admin.site.register(ChatFile, ChatFileAdmin)

class DeliverFilesAdmin(ModelAdmin):
    list_display = ["FileFrom", "FileTo"]
    search_fields = ["FileFrom__username", "FileTo__username"]
    list_filter = ["FileFrom", "FileTo"]


admin.site.register(DeliverFiles, DeliverFilesAdmin)

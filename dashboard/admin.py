from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from dashboard.models import Profile, FollowUser, PrimaryEmail, UserPhone


class ProfileAdmin(ModelAdmin):
    list_display = ["user", "gender", "location", "birth_day"]
    search_fields = ["user__username", "gender", "location"]
    list_filter = ["gender", "location"]


admin.site.register(Profile, ProfileAdmin)

class UserPhoneAdmin(ModelAdmin):
    list_display = ["verified","user", "phone"]
    search_fields = ["user__username", "phone"]
    list_filter = ["verified","user", "phone"]


admin.site.register(UserPhone, UserPhoneAdmin)


class PrimaryEmailAdmin(ModelAdmin):
    list_display = ["user", "email"]
    search_fields = ["user__username", "email"]
    list_filter = ["user", "email"]


admin.site.register(PrimaryEmail, PrimaryEmailAdmin)


class FollowUserAdmin(ModelAdmin):
    list_display = ["profile", "Followed_by"]
    search_fields = ["profile__user__username", "Followed_by__username"]
    list_filter = ["profile", "Followed_by"]


admin.site.register(FollowUser, FollowUserAdmin)

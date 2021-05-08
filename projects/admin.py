from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Project, Bid, categories, Order, CompletedOrder, EmailSubscription, EmailRequest

class OrderAdmin(ModelAdmin):
    list_display = ["creator", "worker", "bid"]
    search_fields = ["creator__username", "worker__username", "bid__project__name"]
    list_filter = ["creator", "worker", "bid"]

class CompletedOrderAdmin(ModelAdmin):
    list_display = ["user", "order", "completed_on"]
    search_fields = ["user__username","created_by__username", "order", "completed_on"]
    list_filter = ["user", "order", "completed_on"]

class ProjectAdmin(ModelAdmin):
    list_display = ["name", "category", "created_by"]
    search_fields = ["name", "category__name", "created_by__username"]
    list_filter = ["name", "category", "created_by"]

class BidAdmin(ModelAdmin):
    list_display = ["project","created_by", "budget"]
    search_fields = ["budget", "description", "created_by__username", "project__name"]
    list_filter = ["budget", "description", "created_by"]

class categoriesAdmin(ModelAdmin):
    list_display = ["name", "image"]
    search_fields = ["name", "image"]
    list_filter = ["name", "image"]


class EmailSubscriptionAdmin(ModelAdmin):
    list_display = ["profile", "email_type", "number_of_emails", "no_of_emails_send"]
    search_fields = ["profile__user__username", "email_type"]
    list_filter = ["email_type"]
    
class EmailRequestAdmin(ModelAdmin):
    list_display = ["profile","expiry_date", "completed", "number_of_emails"]
    search_fields = ["profile__user__username"]
    list_filter = ["completed", "expiry_date"]



admin.site.register(Order, OrderAdmin)
admin.site.register(CompletedOrder, CompletedOrderAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(categories, categoriesAdmin)
admin.site.register(EmailSubscription, EmailSubscriptionAdmin)
admin.site.register(EmailRequest, EmailRequestAdmin)

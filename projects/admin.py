from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Project, Bid, categories, Order, CompletedOrder

class OrderAdmin(ModelAdmin):
    list_display = ["creator", "worker", "bid"]
    search_fields = ["creator", "worker", "bid"]
    list_filter = ["creator", "worker", "bid"]


admin.site.register(Order, OrderAdmin)

class CompletedOrderAdmin(ModelAdmin):
    list_display = ["user", "order", "completed_on"]
    search_fields = ["user", "order", "completed_on"]
    list_filter = ["user", "order", "completed_on"]


admin.site.register(CompletedOrder, CompletedOrderAdmin)

class ProjectAdmin(ModelAdmin):
    list_display = ["name", "category", "created_by"]
    search_fields = ["name", "category", "created_by", "members"]
    list_filter = ["name", "category", "created_by"]


admin.site.register(Project, ProjectAdmin)


class BidAdmin(ModelAdmin):
    list_display = ["budget", "description", "created_by"]
    search_fields = ["budget", "description", "created_by"]
    list_filter = ["budget", "description", "created_by"]


admin.site.register(Bid, BidAdmin)


class categoriesAdmin(ModelAdmin):
    list_display = ["name", "image"]
    search_fields = ["name", "image"]
    list_filter = ["name", "image"]


admin.site.register(categories, categoriesAdmin)

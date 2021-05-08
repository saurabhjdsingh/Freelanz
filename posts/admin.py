from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from posts.models import MyPost, PostComment, PostLike


class MyPostAdmin(ModelAdmin):
    list_display = ["subject", "created_at", "uploaded_by"]
    search_fields = ["subject", "message", "uploaded_by__user__username"]
    list_filter = ["created_at", "uploaded_by"]


admin.site.register(MyPost, MyPostAdmin)


class PostCommentAdmin(ModelAdmin):
    list_display = ["post", "message"]
    search_fields = ["post__id", "message", "comented_by__username"]
    list_filter = ["created_at", "flag"]


admin.site.register(PostComment, PostCommentAdmin)


class PostLikeAdmin(ModelAdmin):
    list_display = ["post", "Liked_by"]
    search_fields = ["post__id", "Liked_by__username"]
    list_filter = ["created_at"]


admin.site.register(PostLike, PostLikeAdmin)

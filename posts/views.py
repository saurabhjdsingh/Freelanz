from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponseRedirect
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.views.generic.edit import CreateView, DeleteView
from braces.views import SelectRelatedMixin
from .models import MyPost, PostLike
from dashboard.models import FollowUser
from . import models
from django.contrib.auth import get_user_model
User = get_user_model()


class UserPostList(LoginRequiredMixin, SelectRelatedMixin, generic.ListView):
    login_url = "accounts:signin"
    raise_exception = False

    model = models.MyPost
    select_related = ('uploaded_by',)
    context_object_name = 'myposts'
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        si = self.request.GET.get("si")
        if si is None:
            si = ""
        user = User.objects.get(username=self.kwargs['username'])
        postList = MyPost.objects.filter(Q(
            uploaded_by=user.profile)).filter(Q(subject__icontains=si)|Q(message__icontains=si)).order_by("-id");

        for p1 in postList:
            p1.liked = False
            ob = PostLike.objects.filter(post=p1, Liked_by=self.request.user.profile.user)
            if ob:
                p1.liked = True
        return postList


class MyPostCreate(LoginRequiredMixin, CreateView):
    login_url = "accounts:signin"
    raise_exception = False

    model = models.MyPost
    fields = ["pic", "subject", "message"]

    def form_valid(self, form):
        self.object = form.save()
        self.object.uploaded_by = self.request.user.profile
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    context_object_name = 'form'
    template_name = 'posts/mypost_form.html'


class LikedPostList(LoginRequiredMixin, SelectRelatedMixin, generic.ListView):
    login_url = "accounts:signin"
    raise_exception = False

    model = models.PostLike
    select_related = ('Liked_by',)
    context_object_name = 'myposts'
    template_name = 'posts/liked_post_list.html'

    def get_context_data(self, **kwargs):
        context = generic.ListView.get_context_data(self, **kwargs)
        postList = PostLike.objects.filter(Liked_by=self.request.user.profile.user).order_by("-id");
        context["myposts"] = postList
        return context


class PostList(LoginRequiredMixin, TemplateView):
    login_url = "accounts:signin"
    raise_exception = False

    template_name = 'posts/post_list.html'

    def get_context_data(self, **kwargs):
        context = TemplateView.get_context_data(self, **kwargs)
        followedList = FollowUser.objects.filter(Followed_by=self.request.user)
        followedList2 = []
        for e in followedList:
            followedList2.append(e.profile)
        postList = MyPost.objects.filter(uploaded_by__in=followedList2).order_by("-id")

        for p1 in postList:
            p1.liked = False
            ob = PostLike.objects.filter(post=p1, Liked_by=self.request.user.profile.user)
            if ob:
                p1.liked = True
            obList = PostLike.objects.filter(post=p1)
            p1.likedno = obList.count()
        context["myposts"] = postList
        return context


class PostDetailView(LoginRequiredMixin, DetailView):
    login_url = "accounts:signin"
    raise_exception = False

    model = MyPost
    context_object_name = 'form'
    template_name = 'posts/post_detail.html'


class MyPostDeleteView(LoginRequiredMixin, DeleteView):
    login_url = "accounts:signin"
    raise_exception = False

    model = MyPost
    context_object_name = 'form'
    template_name = 'posts/post_confirm_delete.html'


def like(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.create(post=post, Liked_by=req.user.profile.user)
    return HttpResponseRedirect(redirect_to="/posts/")


def unlike(req, pk):
    post = MyPost.objects.get(pk=pk)
    PostLike.objects.filter(post=post, Liked_by=req.user.profile.user).delete()
    return HttpResponseRedirect(redirect_to="/posts/")

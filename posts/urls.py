from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path("<str:username>", views.UserPostList.as_view(), name="posts"),
    path("", views.PostList.as_view(), name="allposts"),
    path('create/',
         views.MyPostCreate.as_view(success_url="/posts/"), name="createpost"),
    path('<int:pk>/', views.PostDetailView.as_view(),
         name="detailpost"),
    path('like/<int:pk>', views.like),
    path("liked/", views.LikedPostList.as_view(), name="likedposts"),
    path('unlike/<int:pk>', views.unlike),
    path('delete/<int:pk>',
         views.MyPostDeleteView.as_view(success_url="/posts/"),
         name="deleteposts"),
]

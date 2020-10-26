from django.urls import path

from . import views
app_name = "chat"
urlpatterns = [
    path('<str:username>', views.room, name='room'),
    path('files/<str:username>', views.chatfiles, name='chatfiles'),
    path('video/', views.video, name="video"),
    path('hire/', views.hire, name="hire"),
    path('editbid/', views.edit_bid, name="editbid"),
    path('deliver/', views.deliver, name="deliver"),
    path('complete/', views.complete, name="complete"),
    path('join/', views.joincall, name="joincall")
]
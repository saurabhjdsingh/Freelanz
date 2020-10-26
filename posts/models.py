from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model
from dashboard.models import Profile
User = get_user_model()


class MyPost(models.Model):
    pic = models.ImageField(
        upload_to="users/post_images/%y/%m/%d",
        null=True
    )
    subject = models.CharField(max_length=200)
    message = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(to=Profile, on_delete=CASCADE, null=True)

    def __str__(self):
        return "%s" % self.subject


class PostComment(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    message = models.CharField(max_length=500)
    comented_by = models.ForeignKey(to=User, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    flag = models.CharField(max_length=20, null=True, blank=True,
                            choices=
                            (
                                ("racist", "racist"),
                                ("abusing", "abusing")
                            ))

    def __str__(self):
        return "%s" % self.message


class PostLike(models.Model):
    post = models.ForeignKey(to=MyPost, on_delete=CASCADE)
    Liked_by = models.ForeignKey(to=User, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.Liked_by



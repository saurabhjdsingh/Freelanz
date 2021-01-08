from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True,
                                on_delete=models.CASCADE)
    gender = models.CharField(max_length=200, null=True, blank=True)
    organization_name = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    birth_day = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to="users/profile/%y/%m/%d",
                              default="users/person_1.png")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

#     def save(self, *args, **kwargs):
#         super(Profile, self).save(*args, **kwargs)

#         img = Image.open(self.image.path)

#         if img.height > 200 or img.width > 200:
#             output_size = (200, 200)
#             img.thumbnail(output_size)
#             img.save(self.image.path)

    def get_absolute_url(self):
        return reverse("dashboard:profile", kwargs={'pk': self.pk})


class PrimaryEmail(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(max_length=240, default="example@email.com")
    token = models.CharField(max_length=12, null=True)
    verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    errors = models.IntegerField(default=0)


@receiver(models.signals.post_save, sender=User)
def post_save_user_signal(sender, instance, created, **kwargs):
    if created:
        instance.save()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


class UserPhone(models.Model):
    phone = models.CharField(max_length=15,
                             unique=True,
                             null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    token = models.CharField(max_length=12, null=True)
    verified = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    errors = models.IntegerField(default=0)


class FollowUser(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    Followed_by = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % self.Followed_by

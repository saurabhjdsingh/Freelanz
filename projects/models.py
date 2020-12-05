from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from django import template
User = get_user_model()
register = template.Library()


class categories(models.Model):
    name = models.CharField(max_length=60)
    image = models.ImageField(upload_to="categores",
                              default="users/person_1.png")

    def __str__(self):
        return str(self.name)


class Project(models.Model):
    name = models.CharField(max_length=60, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    budget = models.FloatField()
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to="users/projects/%y/%m/%d", null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    end_date = models.DateField()
    slug = models.SlugField(allow_unicode=True, unique=True)
    category = models.ForeignKey(to=categories, related_name="project_category", on_delete=models.CASCADE)
    bids = models.ManyToManyField(User, related_name="project_bids", through="Bid")
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["name"]


class Bid(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    budget = models.FloatField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=255, null=True, blank=True)
    date_time = models.DateField()

    def __str__(self):
        return str(self.created_by)


class Order(models.Model):
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name="worker")

    created_on = models.DateField(auto_now=True)
    paid = models.FloatField(default=0)

    def __str__(self):
        return str(self.creator)


class CompletedOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    order = models.CharField(max_length=240)
    budget = models.FloatField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer")
    completed_on = models.DateTimeField(auto_now=True)

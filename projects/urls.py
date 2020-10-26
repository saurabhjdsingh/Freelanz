from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = "projects"
urlpatterns = [
    path("", views.Projects, name="projects"),
    path("my", views.Myprojects, name="my_project"),
    path("new/", views.CreateProject, name="create"),
    path("category", views.category, name="category"),
    path("<str:category>", views.Category_Project, name="category_project"),
    path("project/<str:slug>", views.Slug_Project, name="slug_project"),
    path("apply/<slug:project>", views.BidProject, name="bid_project"),
    path("bids/<slug:project>", views.Applicants, name="applicants"),
    path("orders/", views.orders, name="orders")
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

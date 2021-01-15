from django.conf.urls import include
from django.contrib import admin
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.conf import settings
from django.urls import path
from . import views
from . import contact
urlpatterns = [
    path('payments/', include('payments.urls', namespace="payments")),
    path('chat/', include('chat.urls', namespace="chat")),
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('', include('django.contrib.auth.urls')),
    path('', include("accounts.urls", namespace="accounts")),
    path('', include("dashboard.urls", namespace="dashboard")),
    path('contact', contact.contact, name='contact'),
    path('terms', views.terms, name='terms'),
    path('partners', views.partners, name='partners'),
    path('privacy', views.privacy, name='privacy'),
    path('posts/', include("posts.urls", namespace="posts")),
    path('projects/', include("projects.urls", namespace="projects")),
    path('accounts/', include('allauth.urls')),
    path('favicon.ico', RedirectView.as_view(url='/static/pics/favicon.ico')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "thinkgroupy.views.handler404"
handler500 = "thinkgroupy.views.handler500"

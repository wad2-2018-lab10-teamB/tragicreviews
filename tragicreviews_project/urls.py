"""tragicreviews_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from tragicreviews import views
from tragicreviews.regbackend import MyRegistrationView, update_profile, delete_account, delete_account_done
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/register/$', MyRegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/profile/edit/$', update_profile, name='update_profile'),
    url(r'^accounts/account/delete/$', delete_account, name='delete_account'),
    url(r'^accounts/account/delete/done/$', delete_account_done, name='delete_account_done'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    url(r'^tragicreviews/', include('tragicreviews.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




from django.conf.urls import url
from tragicreviews import views
from tragicreviews.regbackend import update_profile, delete_account, delete_account_done

urlpatterns = [
    url(r'^category/(?P<category_name_slug>[\w\-]+)/article/(?P<article_id>\d+)/$', views.article, name='article'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_article/$', views.add_article, name='add_article'),
    url(r'^profile/(?P<profile_id>[\w\-\.\+@]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<profile_id>[\w\-\.\+@]+)/reviews/$', views.profile_reviews, name='profile_reviews'),
    url(r'^profile/(?P<profile_id>[\w\-\.\+@]+)/uploads/$', views.profile_uploads, name='profile_uploads'),
    url(r'^$', views.index, name='index'),
    url(r'^update_profile/$', update_profile, name='update_profile'),
    url(r'^delete_account/$', delete_account, name='delete_account'),
    url(r'^delete_account_done/$', delete_account_done, name='delete_account_done'),
]

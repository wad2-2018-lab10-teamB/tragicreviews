from django.conf.urls import url
from tragicreviews import views

urlpatterns = [
    url(r'^category/(?P<category_name_slug>[\w\-]+)/article/(?P<article_id>\d+)/$', views.article, name='article'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add-article/$', views.add_article, name='add_article'),
    url(r'^profile/(?P<profile_id>[\w\-\.\+@]+)/$', views.profile, name='profile'),
    url(r'^profile/(?P<profile_id>[\w\-\.\+@]+)/reviews/$', views.profile_reviews, name='profile_reviews'),
    url(r'^profile/(?P<profile_id>[\w\-\.\+@]+)/uploads/$', views.profile_uploads, name='profile_uploads'),
    url(r'^$', views.index, name='index'),
    url(r'^add-category/$', views.add_category, name='add_category'),
]

from django.conf.urls import url
from tragicreviews import views
from tragicreviews.regbackend import update_profile

urlpatterns = [
    url(r'^article/$', views.article, name='article'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_article/$', views.add_article, name='add_article'),
    # url(r'^/tragicreviews/$', views.index, name='index'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile_reviews/$', views.profile_reviews, name='profile_reviews'),
    url(r'^profile_uploads/$', views.profile_uploads, name='profile_uploads'),
    url(r'^$', views.index, name='index'),

    url(r'^update_profile/$', update_profile, name='update_profile'),
    # url(r'^restricted/$', views.restricted, name='restricted'),
    # url(r'^category/(?P<category_name_url>\w+)/add_article/$', views.add_page, name='add_page'),
    # #url(r'^search/$', views.search, name='search'),
    # url(r'^goto/$', views.track_url, name='track_url'),
    # url(r'^like_category/$', views.like_category, name='like_category'),
    # url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
    # url(r'^auto_add_page/$', views.auto_add_page, name='auto_add_page'),
	]


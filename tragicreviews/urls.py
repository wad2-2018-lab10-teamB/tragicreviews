from django.conf.urls import url
from tragicreviews import views

urlpatterns = [
    #url(r'^login/$', views.user_login, name='login'),
    # url(r'^restricted/$', views.restricted, name='restricted'),
    #url(r'^logout/$', views.user_logout, name='logout'),
    #url(r'^registration_form/$', views.registration_form, name='registration_form'),
    #url(r'^registration_complete/$', views.registration_complete, name='registration_complete'),
	url(r'^article/$', views.about, name='article'),
	url(r'^category/(?P<category_name_url>\w+)/$', views.category, name='category'),
	url(r'^add_article/$', views.add_article, name='add_article'),
	url(r'^category/(?P<category_name_url>\w+)/add_article/$', views.add_page, name='add_page'),
    url(r'^$', views.index, name='index'),
	#url(r'^search/$', views.search, name='search'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile_reviews/$', views.profile_reviews, name='profile_reviews'),
    url(r'^profile_uploads/$', views.profile_uploads, name='profile_uploads'),
    url(r'^goto/$', views.track_url, name='track_url'),
    # url(r'^like_category/$', views.like_category, name='like_category'),
    # url(r'^suggest_category/$', views.suggest_category, name='suggest_category'),
    # url(r'^auto_add_page/$', views.auto_add_page, name='auto_add_page'),
]

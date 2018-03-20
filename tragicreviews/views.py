# from django.http import HttpResponse, HttpResponseRedirect, Http404
# from django.urls import reverse
from django.shortcuts import redirect, render
# from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from django.bing_search import run_query
# from tragicreviews.template import RequestContext
from tragicreviews.models import Subject, UserProfile, UserLevelField, UserProfileManager, Article, Rating, Comment, ArticleViews
from tragicreviews.forms import UserRegistrationForm, SubjectForm, ArticleForm, CommentForm
from datetime import datetime
from tragicreviews.helperFunctions import *

def encode_url(str):
    return str.replace(' ', '_')
def decode_url(str):
    return str.replace('_', ' ')

@login_required
def add_article(request):

    context_dict = {'categories': []}
    subjects = Subject.objects.all()

    for subject in subjects:
        context_dict['categories'].append(subject)

    return render(request, '/tragicreviews/add_article.html', context_dict)


def article(request, req_title):
    context_dict = {'title': [], 'author':"", 'text':"", }
    # 'comment_author': "", 'comment_date':"", 'comment_author_pic':""

    article_object = Article.objects.filter(title = req_title)
    if article_object.exists():
        context_dict['title'] = article_object.title
        context_dict['author'] = article_object.author
        context_dict['text'] = article_object.body
        # according to bo :P
        context_dict.update('comment_set':[Comment.objects.get(article = article_object)])
    else:
        return False

    return render(request, 'tragicreviews/article.html', context_dict)


def base(request):
    context_dict = {}
    return render(request, 'tragicreviews/base.html', context_dict)


def base_bootstrap(request):
    context_dict = {'categories': []}

    subjects = Subject.name.all()

    for subject in subjects:
        context_dict['categories'].append(subject)


    return render(request, 'tragicreviews/base_bootstrap.html', context_dict)


def category(request, req_cat):
    #Needs a title, author and preview
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        articles = Article.objects.filter(category=category)

        context_dict['articles'] = articles
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'tragicreviews/category.html', context_dict)


def index(request):

    trend_cat_list = ArticleViews.objects.get_trending_articles(limit=5, days=14)

    for cat in trend_cat_list:
        cat.url = encode_url(cat.name)

    context_dict = {'categories': trend_cat_list}

    return render(request, 'tragicreviews/index.html', context_dict)


def profile(request):
    user_dictionary = {}

    # Map a username to all the user's details
    user_dictionary[UserProfile.user.username] = {
        'user': UserProfile.user.username,
        'image': UserProfile.image if bool(UserProfile.image) else False,
        'levels': UserProfile.level,
        'majors': UserProfile.majors.all(),
    }

    context_dict = {'userProfile': {}}
    loggedUser = UserProfile.objects.get(user=request.user)

    context_dict['userProfile'].update(getUserDetails(loggedUser))

    return render(request, 'tragicreviews/profile.html', context_dict)


def profile_reviews(request):
    context_dict = {}


    return render(request, 'tragicreviews/profile_reviews.html', context_dict)

@login_required
def profile_uploads(request):
    context_dict = {}
    return render(request, 'tragicreviews/profile_uploads.html', context_dict)



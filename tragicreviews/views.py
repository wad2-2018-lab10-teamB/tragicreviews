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
    context_dict = base_bootstrap()

    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            form.save(commit=True)

            return index(request)

        else:

            print(form.errors)

    return render(request, 'tragicreviews/add_article.html', context_dict, {'form': form})


def article(request, req_title):
    context_dict = base_bootstrap()

    context_dict['title'] = []
    context_dict['author'] = ""
    context_dict['text'] = ""
    # 'comment_author': "", 'comment_date':"", 'comment_author_pic':""

    article_object = Article.objects.filter(title = req_title)
    if article_object.exists():
        context_dict['title'] = article_object.title
        context_dict['author'] = article_object.author
        context_dict['text'] = article_object.body

        context_dict['comment_set'] = Comment.objects.filter(article = article_object) # This will return a set rather than a single comment
        context_dict['rating_avg'] = Rating.objects.get_average_rating()
        context_dict['total_views'] = ArticleViews.objects.get_total_views()

    else:
        return False

    return render(request, 'tragicreviews/article.html', context_dict)


def base(request):
    context_dict = base_bootstrap()

    return render(request, 'tragicreviews/base.html', context_dict)

#
# def base_bootstrap(request):
#
#
#     context_dict = {'categories': []}
#
#     subjects = Subject.name.all()
#
#     for subject in subjects:
#         context_dict['categories'].append(subject)
#
#
#     return render(request, 'tragicreviews/base_bootstrap.html', context_dict)


def category(request, category_name_slug):
    context_dict = base_bootstrap()

    #Needs a title, author and preview
    try:
        category = Subject.objects.get(slug=category_name_slug)
        articles = Article.objects.filter(category=category)

        context_dict['articles'] = articles
        context_dict['category'] = category

    except Subject.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'tragicreviews/category.html', context_dict)


def index(request):
    context_dict = base_bootstrap()

    context_dict['username'] = UserProfile.user

    trend_article_list = ArticleViews.objects.get_trending_articles(limit=5, days=14)
    for article in trend_article_list:
        article.url = encode_url(article.title)
    context_dict['trend_articles'] = trend_article_list

    new_article_list = ArticleViews.objects.get_trending_articles(limit=5, days=1)
    for article in new_article_list:
        article.url = encode_url(article.title)
    context_dict['new_articles'] = new_article_list

    return render(request, 'tragicreviews/index.html', context_dict)



def profile(request):
    context_dict = base_bootstrap()

    context_dict['UserProfile'] = {}

    logged_user = UserProfile.objects.get(user=request.user)
    context_dict['UserProfile'].update(getUserDetails(logged_user))

    return render(request, 'tragicreviews/profile.html', context_dict)


def profile_reviews(request):
    context_dict = base_bootstrap()

    context_dict['UserProfile'] = {}
    logged_user = UserProfile.objects.get(user=request.user)
    context_dict['UserProfile'].update(getUserDetails(logged_user))

    context_dict['rating_article'] = Rating.article
    context_dict['rating_user'] = Rating.user
    context_dict['rating_rating'] = Rating.rating

    return render(request, 'tragicreviews/profile_reviews.html', context_dict)

@login_required
def profile_uploads(request):
    context_dict = base_bootstrap()

    logged_user = UserProfile.objects.get(user=request.user)

    context_dict['user_articles'] = Article.objects.filter(author=logged_user)

    return render(request, 'tragicreviews/profile_uploads.html', context_dict)



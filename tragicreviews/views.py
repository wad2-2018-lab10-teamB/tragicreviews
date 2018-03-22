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
def add_article(request, category_name_slug):
    context_dict = {}

    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST)

        try:
            if form.is_valid():
                article = form.save(commit=False)
                article.author = UserProfile.objects.get(user=request.user)
                article.category = Subject.objects.get(slug=category_name_slug)
                article.save()

                return index(request)

            else:
                print(form.errors)

        except Subject.DoesNotExist:
            pass


    context_dict['form'] = form

    return render(request, 'tragicreviews/add_article.html', context_dict)


def article(request, article_id, category_name_slug):
    context_dict = {}

    try:
        article_object = Article.objects.get(id = article_id)
        context_dict['title'] = article_object.title
        context_dict['author'] = article_object.author
        context_dict['text'] = article_object.body
        context_dict['category'] = article_object.category

        context_dict['comment_set'] = Comment.objects.filter(article = article_object) # This will return a set rather than a single comment
        context_dict['rating_avg'] = Rating.objects.get_average_rating(article_object)
        context_dict['total_views'] = ArticleViews.objects.get_total_views(article_object)

        ArticleViews.objects.add_view(article_object)

    except Article.DoesNotExist:
        pass

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        try:
            if form.is_valid():
                comment = form.save(commit=False)
                comment.author = UserProfile.objects.get(user=request.user)
                comment.category = Subject.objects.get(slug=category_name_slug)
                comment.save()
                return index(request)
            else:
                print(form.errors)

        except Subject.DoesNotExist:
            pass
    context_dict['form'] = form

    return render(request, 'tragicreviews/article.html', context_dict)


def base(request):
    context_dict = {}

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
    context_dict = {}

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
    context_dict = {}

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



def profile(request, profile_id):
    context_dict = {}

    user = UserProfile.objects.get_by_username(profile_id)
    context_dict['UserProfile'] = user

    return render(request, 'tragicreviews/profile.html', context_dict)


def profile_reviews(request, profile_id):
    context_dict = {}

    user = UserProfile.objects.get_by_username(profile_id)
    context_dict['UserProfile'] = user

    context_dict['rating_article'] = Rating.article
    context_dict['rating_user'] = Rating.user
    context_dict['rating_rating'] = Rating.rating

    return render(request, 'tragicreviews/profile_reviews.html', context_dict)

def profile_uploads(request, profile_id):
    context_dict = {}

    user = UserProfile.objects.get_by_username(profile_id)
    context_dict['UserProfile'] = user

    context_dict['user_articles'] = Article.objects.filter(author=user)

    return render(request, 'tragicreviews/profile_uploads.html', context_dict)



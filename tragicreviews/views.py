from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from tragicreviews.models import Subject, UserProfile, Article, Rating, Comment, ArticleViews
from tragicreviews.forms import ArticleForm, CommentForm, RatingForm, SubjectForm, DeleteSubjectForm
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import DeleteView
from django.core.exceptions import PermissionDenied


@login_required
def add_article(request, category_name_slug):
    context_dict = {}

    category = get_object_or_404(Subject, slug=category_name_slug)

    form = ArticleForm()

    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = UserProfile.objects.get(user=request.user)
            article.category = category
            article.save()

            return HttpResponseRedirect(reverse('article', args=[article.category.slug, article.id]))
        else:
            print(form.errors)

    context_dict['form'] = form

    return render(request, 'tragicreviews/add_article.html', context_dict)


def article(request, article_id, category_name_slug):
    context_dict = {}

    article_object = get_object_or_404(Article, id=article_id)

    ArticleViews.objects.add_view(article_object)

    if request.user.is_authenticated():
        form = CommentForm(prefix="com")
        sub_form = RatingForm(prefix="rev")
        user_profile = UserProfile.objects.get(user=request.user)

        # Was the rating form submitted?
        if request.method == 'POST' and 'ratingbtn' in request.POST:
            # Find an existing rating to update, if available.
            try:
                rating = Rating.objects.get(user=user_profile, article=article_object)
            except Rating.DoesNotExist:
                rating = None

            sub_form = RatingForm(request.POST, prefix="rev", instance=rating)
            if sub_form.is_valid():
                review = sub_form.save(commit=False)
                review.user = user_profile
                review.article = article_object
                review.save()

                return HttpResponseRedirect(request.path_info)
            else:
                print(form.errors)
        
        # Was the comment form submitted?
        if request.method == 'POST' and 'commentbtn' in request.POST:
            form = CommentForm(request.POST, prefix="com")
            if form.is_valid():
                comment = form.save(commit=False)
                comment.user = user_profile
                comment.article = article_object
                comment.save()

                return HttpResponseRedirect(request.path_info)
            else:
                print(form.errors)
            
        context_dict['form'] = form
        context_dict['sub_form'] = sub_form


    context_dict['article'] = article_object

    context_dict['comment_set'] = Comment.objects.filter(article=article_object) # This will return a set rather than a single comment
    context_dict['rating_avg'] = Rating.objects.get_average_rating(article_object)
    context_dict['total_views'] = ArticleViews.objects.get_total_views(article_object)

    return render(request, 'tragicreviews/article.html', context_dict)


@login_required
def edit_article(request, article_id, category_name_slug):
    context_dict = {}

    article = get_object_or_404(Article, id=article_id)
    if request.user != article.author.user:
        raise PermissionDenied("You are not allowed to edit this article.")

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('article', args=[category_name_slug, article_id]))
        else:
            print(form.errors)
    else:
        form = ArticleForm(instance=article)

    context_dict['form'] = form

    return render(request, 'tragicreviews/edit_article.html', context_dict)


class DeleteArticleView(DeleteView, LoginRequiredMixin):
    model = Article
    template_name = 'tragicreviews/generic_confirm_delete.html'
    success_url = reverse_lazy('index')
    slug_field = 'id'
    slug_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        article = super().get_object()
        if self.request.user != article.author.user:
            raise PermissionDenied("You are not allowed to delete this article.")
        return article


def category(request, category_name_slug):
    context_dict = {}

    category = get_object_or_404(Subject, slug=category_name_slug)
    articles = category.get_articles()

    context_dict['articles'] = articles
    context_dict['category'] = category

    return render(request, 'tragicreviews/category.html', context_dict)


def index(request):
    context_dict = {}
    context_dict['trend_articles'] = ArticleViews.objects.get_trending_articles(limit=5, days=14)
    context_dict['new_articles'] = Article.objects.get_new_articles(limit=5)
    return render(request, 'tragicreviews/index.html', context_dict)


def sitemap(request):
    return render(request, 'tragicreviews/sitemap.html')


def profile(request, profile_id):
    context_dict = {}

    try:
        user = UserProfile.objects.get_by_username(profile_id)
        context_dict['user_profile'] = user
    except UserProfile.DoesNotExist:
        raise Http404

    return render(request, 'tragicreviews/profile.html', context_dict)


def profile_reviews(request, profile_id):
    context_dict = {}
    
    try:
        user = UserProfile.objects.get_by_username(profile_id)
        context_dict['user_profile'] = user
        context_dict['ratings'] = Rating.objects.filter(user=user)
    except UserProfile.DoesNotExist:
        raise Http404

    return render(request, 'tragicreviews/profile_reviews.html', context_dict)


def profile_uploads(request, profile_id):
    context_dict = {}
    
    try:
        user = UserProfile.objects.get_by_username(profile_id)
        context_dict['user_profile'] = user
        context_dict['user_articles'] = Article.objects.filter(author=user)
    except UserProfile.DoesNotExist:
        raise Http404

    return render(request, 'tragicreviews/profile_uploads.html', context_dict)


@permission_required('tragicreviews.add_subject', raise_exception=True)
def add_category(request):
    context_dict = {}
    form = SubjectForm()
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect(reverse('index'))  # redirect user to index page
        else:
            print(form.errors)
    context_dict['form'] = form
    return render(request, 'tragicreviews/add_category.html', context_dict)


@permission_required('tragicreviews.delete_subject', raise_exception=True)
def delete_category(request, category_name_slug):
    context_dict = {}

    subject = get_object_or_404(Subject, slug=category_name_slug)
    if request.method == 'POST':
        form = DeleteSubjectForm(request.POST)
        if form.is_valid():
            # All articles under that category will be deleted
            Subject.objects.filter(slug=subject.slug).delete()
            Article.objects.filter(category=subject).delete()
            return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
    else:
        form = DeleteSubjectForm()
    context_dict['form'] = form
    return render(request, 'tragicreviews/subject_confirm_delete.html', context_dict)


@permission_required('tragicreviews.change_subject', raise_exception=True)
def update_category(request, category_name_slug):
    context_dict = {}

    subject = get_object_or_404(Subject, slug=category_name_slug)
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            new_category_name = form.cleaned_data['name']
            for a in Article.objects.filter(category=subject):
                a.category = Subject.objects.get(name=new_category_name)
                a.save()
            for u in UserProfile.objects.all():
                if u.majors.filter(name=subject):
                    u.majors.add(Subject.objects.get(name=new_category_name))
                    u.majors.remove(subject)
                    u.save()
            # Remove all articles under new category and delete old one
            Subject.objects.filter(slug=subject.slug).delete()
            return HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
    else:
        form = SubjectForm()
    context_dict['form'] = form
    return render(request, 'tragicreviews/update_category.html', context_dict)

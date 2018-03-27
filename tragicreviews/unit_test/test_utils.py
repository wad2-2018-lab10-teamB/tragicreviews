from tragicreviews.models import *
from django.contrib.auth.models import Permission


def create_groups():
    Group.objects.get_or_create(name="student")
    staff = Group.objects.get_or_create(name="staff")[0]
    staff.permissions.add(Permission.objects.get(codename="add_subject"))
    staff.permissions.add(Permission.objects.get(codename="change_subject"))
    staff.permissions.add(Permission.objects.get(codename="delete_subject"))
    staff.save()


def create_subject():
    s = Subject(name="foo")
    s.save()
    return s


def create_user():
    user_pf = UserProfile.objects.create_user("dummy")
    return user_pf


def create_article():
    s = Subject(name="bar")
    s.save()
    user_pf = UserProfile.objects.create_user("zombie")
    title = "Title"
    body = "Hello World!"
    a = Article(category=s, title=title, author=user_pf, body=body)
    a.save()
    return a


def create_article_views():
    a = create_article()
    article_views = ArticleViews(article=a, views=100)
    article_views.save()


def create_article_for_testing_article_view():
    a = create_article()
    user_pf = UserProfile.objects.get_by_username("zombie")
    comment_text = "This is a comment"
    comment = Comment(user=user_pf, article=a, text=comment_text)
    comment.save()
    rating = Rating(user=user_pf, article=a, rating=4)
    rating.save()
    article_views = ArticleViews(article=a, views=100)
    article_views.save()


def create_user_profile_for_testing():
    user_pf = create_user()
    user_pf.user.set_password('test1234')
    user_pf.user.email = 'test@test.com'
    user_pf.user.save()
    user_pf.save()
    subject = create_subject()
    title = "User Article"
    body = "User article content"
    user_article = Article(author=user_pf, category=subject, title=title, body=body)
    user_article.save()

    other_article = create_article()
    rating1 = Rating(user=user_pf, article=other_article, rating=4)
    rating2 = Rating(user=user_pf, article=user_article, rating=5)
    rating1.save()
    rating2.save()
    return user_pf.user.username


def create_student_user_profile():
    create_groups()
    user_pf = create_user()
    user_pf.user.set_password('test1234')
    group = Group.objects.get(name='student')
    user_pf.user.groups.add(group)
    user_pf.user.save()
    user_pf.save()
    return user_pf.user.username


def create_staff_user_profile():
    create_groups()
    user_pf = create_user()
    user_pf.user.set_password('test1234')
    group = Group.objects.get(name='staff')
    user_pf.user.groups.add(group)
    user_pf.user.save()
    user_pf.save()
    return user_pf.user.username

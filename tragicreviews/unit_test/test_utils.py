from tragicreviews.models import *


def create_subject():
    s = Subject(name="foo")
    s.save()
    return s


def create_user():
    user_pf = UserProfile.objects.create_user("dummy")
    return user_pf


def create_article():
    s = Subject(name="bar")
    user_pf = UserProfile.objects.create_user("zombie")
    title = "Title"
    body = "Hello World!"
    a = Article(category=s, title=title, author=user_pf, body=body)
    a.save()
    return a



from django.test import TestCase
from tragicreviews.models import Subject, Article, Rating, Comment, UserProfile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.db import transaction
import tragicreviews.unit_test.test_utils as test_utils

# Testing Models
class ModelTests(TestCase):

    def test_creating_category(self):
        s = Subject(name="Computing Science")
        s.save()
        subjects = Subject.objects.all()
        # Test subject is generated
        self.assertEqual(len(subjects), 1)
        # Test subject is saved correctly
        self.assertEqual(subjects[0], s)
        # Test slug is correct
        self.assertEqual(subjects[0].slug, "computing-science")

    def test_creating_user_profile(self):
        user_pf = test_utils.create_user()
        UserProfile.objects.create_user("mummy")
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(UserProfile.objects.all().count(), 2)
        self.assertEqual(UserProfile.objects.all()[0], user_pf)

    def test_creating_article(self):
        user_pf = test_utils.create_user()
        s = Subject(name="Computing Science")
        s.save()
        # Create 2 articles for testing
        # Article one
        body_one = "Hello World!"
        article_one = Article(title="Terrible Code", body=body_one, author=user_pf)
        article_one.category = s
        article_one.save()
        # Article two
        body_two = "Goodbye World!"
        article_two = Article(title="Even More Terrible Code", body=body_two, author=user_pf)
        article_two.category = s
        article_two.save()

        articles = s.article_set.all()
        # Test the number of articles is correct
        self.assertEqual(articles.count(), 2)
        # Test articles are saved correctly
        self.assertEqual(articles[0], article_one)
        # Test article title is saved correctly
        self.assertEqual(articles[0].title, article_one.title)
        # Test article body is saved correctly
        self.assertEqual(articles[0].body, article_one.body)
        # Test article author is saved correctly
        self.assertEqual(articles[0].author, article_one.author)
        # Test article category is saved correctly
        self.assertEqual(articles[0].category, s)

    def test_rating(self):
        user = test_utils.create_user()
        article = test_utils.create_article()
        neg_val = -1
        zero_val = 0
        large_val = 6

        # test creating rating
        rating0 = Rating(user=user, article=article, rating=3)
        rating0.save()
        self.assertEqual(Rating.objects.all().count(), 1)
        self.assertEqual(Rating.objects.all()[0].rating, 3)
        self.assertEqual(Rating.objects.all()[0].user, user)
        self.assertEqual(Rating.objects.all()[0].article, article)

        rating1 = Rating(user=user, article=article, rating=4)

        # test integrity
        with transaction.atomic():
            self.assertRaises(IntegrityError, lambda: rating1.save())
        Rating.objects.all().delete()

        # test a rating with negative value
        rating2 = Rating(user=user, article=article, rating=neg_val)
        self.assertRaises(ValidationError, lambda: rating2.full_clean())

        # test a rating with zero value
        rating3 = Rating(user=user, article=article, rating=zero_val)
        self.assertRaises(ValidationError, lambda: rating3.full_clean())

        # test a rating with value larger than max value
        rating4 = Rating(user=user, article=article, rating=large_val)
        self.assertRaises(ValidationError, lambda: rating4.full_clean())

    def test_comment(self):
        text = "Testing..."
        user = test_utils.create_user()
        article = test_utils.create_article()
        comment = Comment(user=user, article=article, text=text)
        comment.save()
        self.assertEqual(Comment.objects.all().count(), 1)
        self.assertEqual(Comment.objects.all()[0].text, text)
        self.assertEqual(Comment.objects.all()[0].article, article)
        self.assertEqual(Comment.objects.all()[0].user, user)

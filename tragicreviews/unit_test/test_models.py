from django.test import TestCase
from tragicreviews.models import Subject, Article, Rating, Comment, UserProfile, UserLevelField, ArticleViews
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
import tragicreviews.unit_test.test_utils as test_utils
from datetime import datetime
from django.db.utils import IntegrityError
from django.db import transaction
from freezegun import freeze_time
from io import StringIO
import sys


# Testing Models
class ModelTests(TestCase):

    def test_create_category(self):
        s = Subject(name="Computing Science")
        s.save()
        subjects = Subject.objects.all()
        # Test subject is generated
        self.assertEqual(len(subjects), 1)
        # Test subject is saved correctly
        self.assertEqual(subjects[0], s)
        # Test slug is correct
        self.assertEqual(subjects[0].slug, "computing-science")

    def test_create_user_profile(self):
        user_pf = test_utils.create_user()
        UserProfile.objects.create_user("mummy")
        self.assertEqual(User.objects.all().count(), 2)
        self.assertEqual(UserProfile.objects.all().count(), 2)
        self.assertEqual(UserProfile.objects.all()[0], user_pf)

        # Test one to one field on deletion
        # Delete a user, the user profile will also be deleted
        User.objects.all().delete()
        self.assertEqual(UserProfile.objects.all().count(), 0)

        # Delete a user profile, the user will also be deleted
        UserProfile.objects.create_user("mummy")
        UserProfile.objects.all().delete()
        self.assertEqual(User.objects.all().count(), 0)

        # Test Integrity
        user_pf1 = UserProfile.objects.create_user("mummy")
        user_pf2 = UserProfile(user=user_pf1.user)
        self.assertRaises(ValidationError, lambda: user_pf2.save())

    def test_get_user_profile_by_username(self):
        user_pf1 = UserProfile.objects.create_user("mummy")
        user_pf2 = UserProfile.objects.create_user("dummy")

        # Test getting correct user according to username
        self.assertEqual(user_pf1, UserProfile.objects.get_by_username("mummy"))
        self.assertNotEqual(user_pf2, UserProfile.objects.get_by_username("mummy"))

    def test_user_profile_group(self):
        test_utils.create_groups()
        user_pf1 = UserProfile.objects.create_user("mummy")
        user_pf2 = UserProfile.objects.create_user("dummy")
        user_pf1.user.groups.add(Group.objects.get(name="staff"))
        user_pf2.user.groups.add(Group.objects.get(name="student"))
        user_pf1.save()
        user_pf2.save()

        # Test checking user group
        self.assertTrue(UserProfile.is_member(user_pf1, "staff"))
        self.assertFalse(UserProfile.is_member(user_pf1, "student"))
        self.assertTrue(UserProfile.is_member(user_pf2, "student"))
        self.assertFalse(UserProfile.is_member(user_pf2, "staff"))

        # Test getting correct names of roles
        self.assertEqual(UserProfile.get_role(user_pf1), "Staff")
        self.assertEqual(UserProfile.get_role(user_pf2), "Student")

    def test_user_profile_name_representation(self):
        test_utils.create_groups()
        user_pf1 = UserProfile.objects.create_user("mummy")
        user_pf2 = UserProfile.objects.create_user("dummy")
        user_pf1.user.groups.add(Group.objects.get(name="staff"))
        user_pf2.user.groups.add(Group.objects.get(name="student"))
        user_pf1.save()
        user_pf2.save()

        # Test lecture user profile
        self.held, sys.stdout = sys.stdout, StringIO()
        print(user_pf1)
        self.assertEqual("mummy ✔", sys.stdout.getvalue().strip())

        # Test student user profile
        self.held, sys.stdout = sys.stdout, StringIO()
        print(user_pf2)
        self.assertEqual("dummy", sys.stdout.getvalue().strip())

    def test_create_article(self):
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
        user2 = UserProfile.objects.create_user("another")
        article = test_utils.create_article()
        article2 = Article(title="Even More Terrible Code", body=article.body, author=article.author, category=article.category)
        article2.save()
        neg_val = -1
        zero_val = 0
        large_val = 6

        # Test creating rating
        rating0 = Rating(user=user, article=article, rating=3)
        rating0.save()
        self.assertEqual(Rating.objects.all().count(), 1)
        self.assertEqual(Rating.objects.all()[0].rating, 3)
        self.assertEqual(Rating.objects.all()[0].user, user)
        self.assertEqual(Rating.objects.all()[0].article, article)

        rating1 = Rating(user=user, article=article, rating=4)

        # Test integrity
        self.assertRaises(ValidationError, lambda: rating1.save())

        # Test same user could rate different articles and same article could be rated by different users
        rating2 = Rating(user=user2, article=article, rating=5)
        rating3 = Rating(user=user, article=article2, rating=5)
        self.assertIsNone(rating2.save())
        self.assertIsNone(rating3.save())
        self.assertEqual(Rating.objects.all().count(), 3)

        # Test the number of ratings created by a user is correct
        self.assertEqual(user.rating_set.count(), 2)

        # Test when ratings are deleted, they are also deleted from a user's rating set
        Rating.objects.all().delete()
        self.assertEqual(user.rating_set.count(), 0)

        # Test when a user is deleted, the user's ratings are all also deleted
        rating0 = Rating(user=user2, article=article, rating=3)
        rating0.save()
        rating1 = Rating(user=user2, article=article2, rating=5)
        rating1.save()
        self.assertEqual(Rating.objects.all().count(), 2)
        UserProfile.objects.filter(user=user2.user).delete()
        self.assertEqual(Rating.objects.all().count(), 0)

        # Test a rating with negative value
        rating2 = Rating(user=user, article=article, rating=neg_val)
        self.assertRaises(ValidationError, lambda: rating2.full_clean())

        # Test a rating with zero value
        rating3 = Rating(user=user, article=article, rating=zero_val)
        self.assertRaises(ValidationError, lambda: rating3.full_clean())

        # Test a rating with value larger than max value
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

    def test_user_level_field(self):
        test_utils.create_groups()
        student_levels = UserLevelField.student_levels
        staff_levels = UserLevelField.staff_levels

        # Test correct number of levels
        self.assertEqual(len(student_levels), 6)
        self.assertEqual(len(staff_levels), 5)

        user_pf = test_utils.create_user()
        user_pf.user.groups.add(Group.objects.get(name="student"))
        user_pf.level = staff_levels[0]

        # Test raise error when assigning a staff level to a student account
        self.assertRaises(ValidationError, lambda: user_pf.save())

        # reset
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        user_pf = test_utils.create_user()
        user_pf.user.groups.add(Group.objects.get(name="staff"))
        user_pf.level = student_levels[0]

        # Test raise error when assigning a student level to a staff account
        self.assertRaises(ValidationError, lambda: user_pf.save())

        # reset
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        user_pf = test_utils.create_user()
        user_pf.user.groups.add(Group.objects.get(name="student"))
        user_pf.level = student_levels[0]

        # Test correctness of assigning student level to student account
        # no error raises
        self.assertTrue(user_pf.save() is None)
        # level is saved correctly
        self.assertEqual(user_pf.level, UserLevelField.student_levels[0])

        # reset
        UserProfile.objects.all().delete()
        User.objects.all().delete()
        user_pf = test_utils.create_user()
        user_pf.user.groups.add(Group.objects.get(name="staff"))
        user_pf.level = staff_levels[0]

        # Test correctness of assigning staff level to staff account
        # no error raises
        self.assertTrue(user_pf.save() is None)
        # level is saved correctly
        self.assertEqual(user_pf.level, UserLevelField.staff_levels[0])

    def test_article_views(self):
        article1 = test_utils.create_article()
        article2 = Article(title="Even More Terrible Code", body=article1.body, author=article1.author,
                           category=article1.category)
        article2.save()
        article_views = ArticleViews(article=article1, views=1)
        article_views.save()

        # Test correct number of ArticleViews models
        self.assertEqual(ArticleViews.objects.all().count(), 1)

        article_views2 = ArticleViews(article=article2, views=3)
        article_views2.save()

        # Test correct number of ArticleViews models
        self.assertEqual(ArticleViews.objects.all().count(), 2)

        # Test integrity
        article_views3 = ArticleViews(article=article2, views=45)
        with transaction.atomic():
            self.assertRaises(IntegrityError, lambda: article_views3.save())

        # reset
        ArticleViews.objects.all().delete()
        self.assertEqual(ArticleViews.objects.all().count(), 0)

        # Test different articles could have different views on same date
        article_views = ArticleViews(article=article1, views=5)
        article_views.save()
        article_views4 = ArticleViews(article=article2, views=5)
        self.assertIsNone(article_views4.save())

        # Test same article could have different views on different date
        with freeze_time(lambda: datetime(2018, 2, 4)):
            article_views5 = ArticleViews(article=article1, views=5)
            self.assertIsNone(article_views5.save())
        print(article_views.date)
        print(article_views5.date)



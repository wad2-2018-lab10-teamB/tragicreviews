from django.test import TestCase
from tragicreviews.models import Subject, UserProfile, Article
from django.contrib.auth.models import Group
import populate_tragicreviews

"""
Unit tests for populate scripts
"""


class PopulateTests(TestCase):

    def test_add_subject(self):
        populate_tragicreviews.add_subject("foo")
        populate_tragicreviews.add_subject("bar")
        self.assertEqual(Subject.objects.all().count(), 2)
        self.assertEqual(Subject.objects.filter(name="foo").count(), 1)
        self.assertEqual(Subject.objects.filter(name="bar").count(), 1)

    def test_populate_tragicreviews_core(self):
        # Run core
        populate_tragicreviews.populate_core()
        cats = Subject.objects.all()

        # Tests the number of categories is correct
        self.assertTrue(len(cats) == 13)

        # Tests the number of groups is correct
        groups = Group.objects.all()
        self.assertTrue(len(groups) == 2)

        # Test groups contain student and staff
        self.assertTrue(Group.objects.get(name="student"))
        self.assertTrue(Group.objects.get(name="staff"))

        # test numbers of permissions of staff and student group are correct
        self.assertEqual(Group.objects.get(name="student").permissions.all().count(), 0)
        self.assertEqual(Group.objects.get(name="staff").permissions.all().count(), 3)

        # Test staff group has correct permissions
        staff = Group.objects.get(name="staff")
        self.assertTrue(staff.permissions.get(codename="add_subject"))
        self.assertTrue(staff.permissions.get(codename="change_subject"))
        self.assertTrue(staff.permissions.get(codename="delete_subject"))

    def test_setup_user(self):
        populate_tragicreviews.populate_core()
        populate_tragicreviews.setup_user("staff", 0)
        populate_tragicreviews.setup_user("student", 1)

        # Test correctness of setting up user profiles
        self.assertEqual(UserProfile.objects.all().count(), 2)
        self.assertEqual(UserProfile.objects.filter(user__groups=Group.objects.get(name="staff")).count(), 1)
        self.assertEqual(UserProfile.objects.filter(user__groups=Group.objects.get(name="student")).count(), 1)

    def test_populate_tragicreviews_examples(self):
        # Run core first
        populate_tragicreviews.populate_core()
        # Run examples
        populate_tragicreviews.populate_examples()

        # Test the numbers of staff users an student users are correct
        self.assertEqual(UserProfile.objects.filter(user__groups=Group.objects.get(name="staff")).count(), 5)
        self.assertEqual(UserProfile.objects.filter(user__groups=Group.objects.get(name="student")).count(), 5)

        # Test each category contains at least 1 at most 3 articles
        for cat in Subject.objects.all():
            self.assertGreaterEqual(Article.objects.filter(category=cat).count(), 1)
            self.assertLessEqual(Article.objects.filter(category=cat).count(), 3)

        # Test each article has at least 0 and at most 5 ratings
        for a in Article.objects.all():
            self.assertGreaterEqual(a.rating_set.count(), 0)
            self.assertLessEqual(a.rating_set.count(), 5)

        # Test each article has at least 0 and at most 5 comments
        for a in Article.objects.all():
            self.assertGreaterEqual(a.comment_set.count(), 0)
            self.assertLessEqual(a.comment_set.count(), 5)

        # Test the article author is not one of the raters of an article
        for a in Article.objects.all():
            author = a.author
            self.assertEqual(a.rating_set.filter(user=author).count(), 0)

        # Test the article author is not one of the commenters of an article
        for a in Article.objects.all():
            author = a.author
            self.assertEqual(a.comment_set.filter(user=author).count(), 0)


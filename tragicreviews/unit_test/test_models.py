from django.test import TestCase
from tragicreviews.models import Category, Article, Rating, Comment

# Testing Models
class ModelTests(TestCase):

    def test_creating_category(self):
        c = Category(name="Computing Science")
        c.save()
        cats_in_database = Category.objects.all()
        self.assertEqual(len(cats_in_database), 1)
        self.assertEqual(cats_in_database[0], c)


from django.test import TestCase
from tragicreviews.models import Subject, Article, Rating, Comment


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

    # Currently not functioning
    def test_creating_article(self):
        s = Subject(name="Computing Science")
        s.save()
        # Create 2 articles for testing
        # Article one
        body_one = "Hello World!"
        article_one = Article(title="Terrible Code", body=body_one)
        article_one.category = s
        article_one.save()
        # Article two
        body_two = "Goodbye World!"
        article_two = Article(title="Even More Terrible Code", body=body_two)
        article_two.category = s
        article_two.save()

        articles = s.article_set.all()
        # Test the number of articles is correct
        self.assertEqual(articles.count(), 2)
        # Test articles are saved correctly
        self.assertEqual(articles[0], article_one)
        self.assertEqual(articles[0].title, article_one.title)
        self.assertEqual(articles[0].body, article_one.body)




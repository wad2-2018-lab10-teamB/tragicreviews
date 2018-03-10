from django.test import TestCase
from tragicreviews.models import Subject
import populate_tragicreviews

class PopulateTests(TestCase):

    def test_populate_tragicreviews(self):
        populate_tragicreviews.populate()
        cats = Subject.objects.all()

        # Tests the number of categories is correct
        print(len(cats))
        self.assertTrue(len(cats) == 13)


from django.test import TestCase
import tragicreviews.unit_test.test_utils as test_utils
from tragicreviews.context_processors import subject_list
from django.core.urlresolvers import reverse


"""
Unit Test for classes and functions which are not in main modules (i.e., models, views, etc.)
"""


class TestMiscellanies(TestCase):

    def test_context_processors(self):
        test_utils.create_subject()
        lst = subject_list(self.client.get(reverse('index')))['categories']

        # Test correctness of the number of subjects sent to request
        self.assertEquals(lst.count(), 1)
        self.assertEquals(lst.filter(name="foo").count(), 1)


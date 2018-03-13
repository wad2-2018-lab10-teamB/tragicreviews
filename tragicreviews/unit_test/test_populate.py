from django.test import TestCase
from tragicreviews.models import Subject
from django.contrib.auth.models import Group
import populate_tragicreviews


class PopulateTests(TestCase):

    def test_populate_tragicreviews(self):
        populate_tragicreviews.populate()
        cats = Subject.objects.all()

        # Tests the number of categories is correct
        self.assertTrue(len(cats) == 13)

        # Tests the number of groups is correct
        groups = Group.objects.all()
        self.assertTrue(len(groups) == 2)

        # Test groups contain student and staff
        self.assertTrue(Group.objects.get(name="student"))
        self.assertTrue(Group.objects.get(name="staff"))

        # Test staff group have correct permissions
        staff = Group.objects.get(name="staff")
        self.assertTrue(staff.permissions.get(codename="add_subject"))
        self.assertTrue(staff.permissions.get(codename="change_subject"))
        self.assertTrue(staff.permissions.get(codename="delete_subject"))




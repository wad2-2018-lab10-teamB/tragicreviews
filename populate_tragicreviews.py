import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tragicreviews_project.settings")

import django
django.setup()
from django.contrib.auth.models import Group, Permission
from tragicreviews.models import Category

def populate():
	print("Setting up student and staff groups...")
	Group.objects.get_or_create(name="student")

	staff = Group.objects.get_or_create(name="staff")[0]
	staff.permissions.add(Permission.objects.get(codename="add_category"))
	staff.permissions.add(Permission.objects.get(codename="change_category"))
	staff.permissions.add(Permission.objects.get(codename="delete_category"))
	staff.save()

	# Pre-populate if empty	
	if Category.objects.count() == 0:
		print("Adding default categories...")

		default_categories = [
			"Computing Science",
			"Maths & Stats",
			"Chemistry",
			"Physics",
			"Biology",
			"Engineering",
			"Geography",
			"History",
			"Law",
			"Modern Languages",
			"Music",
			"Psychology",
			"Social and Political Sciences"
		]

		for cat in default_categories:
			add_category(cat)

def add_category(name):
	Category.objects.get_or_create(name=name)
	print("Added category '{}'.".format(name))

if __name__ == "__main__":
	print("Starting TragicReviews population script...")
	populate()
	print("Done!")

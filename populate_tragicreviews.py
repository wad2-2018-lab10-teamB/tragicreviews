import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tragicreviews_project.settings")

import django
django.setup()
from django.contrib.auth.models import Group, Permission
from tragicreviews.models import Subject

def populate():
	print("Setting up student and staff groups...")
	Group.objects.get_or_create(name="student")

	staff = Group.objects.get_or_create(name="staff")[0]
	staff.permissions.add(Permission.objects.get(codename="add_subject"))
	staff.permissions.add(Permission.objects.get(codename="change_subject"))
	staff.permissions.add(Permission.objects.get(codename="delete_subject"))
	staff.save()

	# Pre-populate if empty	
	if Subject.objects.count() == 0:
		print("Adding default subjects...")

		default_subjects = [
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

		for sub in default_subjects:
			add_subject(sub)

def add_subject(name):
	Subject.objects.get_or_create(name=name)
	print("Added subject '{}'.".format(name))

if __name__ == "__main__":
	print("Starting TragicReviews population script...")
	populate()
	print("Done!")

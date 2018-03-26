#!/usr/bin/env python3
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tragicreviews_project.settings")

import django
django.setup()

from django.contrib.auth.models import Group, Permission
from tragicreviews.models import Subject, UserProfile, UserLevelField, Article, Comment, Rating
import random
import sys

def populate_core():
	print("Starting core population...")
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

	print("Finished core population.")

def add_subject(name):
	Subject.objects.get_or_create(name=name)
	print("\tAdded subject '{}'.".format(name))

def populate_examples():
	print("Starting examples population...")

	if UserProfile.objects.count() > 0:
		print("WARNING: Users already exist in database. Skipping examples population...")
		return

	print("Adding example users...")
	example_users = []
	for i in range(5):
		example_users.append(setup_user("student", i + 1))
		example_users.append(setup_user("staff", i + 1))

	print("Adding example articles...")
	example_body = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean ex eros, dignissim eu sollicitudin et, aliquet sit amet libero. "
	"Pellentesque sit amet tellus elementum, consequat dolor quis, facilisis diam. Donec porttitor turpis velit, at dictum mi tincidunt ut. "
	"Nam at risus id enim eleifend posuere. Sed fermentum cursus tempor. Praesent pharetra quam sit amet luctus porttitor. Praesent accumsan justo nec mi varius, "
	"sit amet molestie lacus commodo. Praesent sodales feugiat nunc, sodales rhoncus lorem feugiat id. Suspendisse elementum ex erat, et vestibulum quam aliquet et.")
	for cat in Subject.objects.all():
		for i in range(random.randint(1, 3)):
			author = random.choice(example_users)
			article = Article.objects.create(category=cat, title=f"Example {cat.name} article {i + 1}", body=example_body, author=author)
			print(f"\tAdded \"{article.title}\"")

			possible_commenters = example_users[:]
			possible_commenters.remove(author)
			for i in range(random.randint(0, 5)):
				commenter = random.choice(possible_commenters)
				possible_commenters.remove(commenter)
				Comment.objects.create(article=article, user=commenter, text=f"Example comment {i + 1}")
				print(f"\t\tAdded comment from {commenter.user}")

			possible_raters = example_users[:]
			possible_raters.remove(author)
			for i in range(random.randint(0, 5)):
				rater = random.choice(possible_raters)
				rating = random.randint(1, 5)
				possible_raters.remove(rater)
				Rating.objects.create(article=article, user=rater, rating=rating)
				print(f"\t\tAdded {rating}/5 rating from {rater.user}")

	print("Finished examples population.")

def setup_user(type, i):
	user = UserProfile.objects.create_user(f"example-{type}-{i}", group=type)
	user.image = "profile_images/default_avatar.jpg"
	user.majors = random.sample(list(Subject.objects.all()), random.randint(0, Subject.objects.count()))
	if type == "student":
		user.level = random.choice(UserLevelField.student_levels + [None])
	else:
		user.level = random.choice(UserLevelField.staff_levels + [None])
	user.save()
	print(f"\tAdded user \"{user.user}\"")
	return user

if __name__ == "__main__":
	print("Starting TragicReviews population script...\n")

	mode = ' '.join(sys.argv[1:]).strip()
	if mode != "core" and mode != "examples":
		print("ERROR: Missing mode argument!\n"
		"\n"
		"./populate_tragicreviews.py [mode]\n"
		"\n"
		"This population script takes one parameter: the mode.\n"
		"\n"
		"This may be either \"core\" or \"examples\" (without quotes):\n"
		"- \"core\" sets up the staff and student groups and the core list of subjects. This is required for the application to run properly and is the recommended mode for production deployment.\n"
		"- \"examples\" also runs the core population but in addition sets up 10 example users (5 student, 5 staff) and a random number of articles (1-3) in each category, each with a random number (0-5) of ratings and comments.")
	else:
		populate_core()
		if mode == "examples":
			populate_examples()
		print("\nDone!")

from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, Group
from django.core.validators import MaxValueValidator, MinValueValidator

class Subject(models.Model):
	name = models.CharField(max_length=32, unique=True)
	slug = models.SlugField(max_length=32, primary_key=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super().save(*args, **kwargs)

	def __str__(self):
		return self.name

class UserProfileManager(models.Manager):
	def create_user(self, username, email=None, password=None, group=None, **kwargs):
		user = User.objects.create_user(username, email, password)

		if group:
			user.groups.add(Group.objects.get(name=group))
			user.save(using=self._db)

		user_profile = self.model(user=user)
		user_profile.save(using=self._db)
		return user_profile

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	image = models.ImageField(upload_to='profile_images', blank=True)#null=True)
	majors = models.ManyToManyField(Subject)

	objects = UserProfileManager()

	def __str__(self):
		return self.user.username

class Article(models.Model):
	category = models.ForeignKey(Subject)
	title = models.CharField(max_length=128)
	body = models.TextField(max_length=5000)
	author = models.ForeignKey(UserProfile)

class Rating(models.Model):
	article = models.ForeignKey(Article)
	user = models.ForeignKey(UserProfile)
	rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

	class Meta:
		unique_together = ('article', 'user')

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

class Comment(models.Model):
	article = models.ForeignKey(Article)
	user = models.ForeignKey(UserProfile)
	text = models.TextField(max_length=500)

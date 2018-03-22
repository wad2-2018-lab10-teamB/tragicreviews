from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User, Group
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.utils import timezone
from datetime import timedelta

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

	def get_by_username(self, username):
		return self.get(user=User.objects.get(username=username))

class UserLevelField(models.CharField):
	student_levels = ["Level 1 undergraduate", "Level 2 undergraduate", "Level 3 undergraduate", "Level 4 undergraduate", "Level 5 undergraduate", "Postgraduate"]
	staff_levels = ["Tutor", "Lecturer", "Senior lecturer", "Reader", "Professor"]

	def __init__(self, *args, **kwargs):
		kwargs["max_length"] = 24
		kwargs["blank"] = True
		kwargs["null"] = True
		super().__init__(*args, **kwargs)

	def validate(self, value, model_instance):
		super().validate(value, model_instance)

		if not isinstance(model_instance, UserProfile):
			raise ValidationError("UserLevelField is only supported on UserProfile models.")

		if value is None:
			return

		valid = False
		if model_instance.is_member("student"):
			if value in self.student_levels:
				valid = True
		if not valid and model_instance.is_member("staff"):
			if value in self.staff_levels:
				valid = True
		if not valid:
			raise ValidationError(
				self.error_messages["invalid_choice"],
				code="invalid_choice",
				params={"value": value}
			)

	def deconstruct(self):
		name, path, args, kwargs = super().deconstruct()
		del kwargs["max_length"]
		del kwargs["blank"]
		del kwargs["null"]
		return name, path, args, kwargs

class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	image = models.ImageField(upload_to='profile_images', blank=True)
	level = UserLevelField()
	majors = models.ManyToManyField(Subject)

	objects = UserProfileManager()

	def is_member(self, group):
		return self.user.groups.filter(name=group).exists()

	def get_role(self):
		if self.is_member("staff"):
			return "Staff"
		elif self.is_member("student"):
			return "Student"

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)

	def __str__(self):
		return self.user.username


class Article(models.Model):
	category = models.ForeignKey(Subject)
	title = models.CharField(max_length=128)
	body = models.TextField(max_length=5000)
	author = models.ForeignKey(UserProfile)

	def __str__(self):
		return self.title + " - " + self.category.name


class RatingManager(models.Manager):
	def get_average_rating(self, article):
		return self.filter(article=article).aggregate(models.Avg("rating"))["rating__avg"] or 0

class Rating(models.Model):
	article = models.ForeignKey(Article)
	user = models.ForeignKey(UserProfile)
	rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

	objects = RatingManager()

	class Meta:
		unique_together = ('article', 'user')

	def save(self, *args, **kwargs):
		self.full_clean()
		super().save(*args, **kwargs)


class Comment(models.Model):
	article = models.ForeignKey(Article)
	user = models.ForeignKey(UserProfile)
	text = models.TextField(max_length=500)


class ArticleViewsManager(models.Manager):
	def get_total_views(self, article, *, days=0):
		article_views = self.filter(article=article)
		if days > 0:
			article_views = article_views.filter(date__gt=timezone.now() - timedelta(days=days))

		return article_views.aggregate(models.Sum("views"))["views__sum"] or 0

	def get_trending_articles(self, *, limit=0, days=7):
		article_views = self.values("article")
		if days > 0:
			article_views = article_views.filter(date__gt=timezone.now() - timedelta(days=days))

		trending_articles = article_views.annotate(views=models.Sum("views")).order_by("-views")
		if limit > 0:
			trending_articles = trending_articles[:limit]
		return [Article.objects.get(pk=record["article"]) for record in trending_articles]

class ArticleViews(models.Model):
	article = models.ForeignKey(Article)
	date = models.DateField(auto_now_add=True)
	views = models.PositiveIntegerField()

	objects = ArticleViewsManager()

	class Meta:
		unique_together = ("article", "date")
		verbose_name_plural = "Article views"

	def __str__(self):
		return f"\"{self.article}\" - {self.views} views on {self.date}"

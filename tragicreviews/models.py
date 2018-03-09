from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Category(models.Model):
	name = models.CharField(max_length=32, unique=True)
	slug = models.SlugField(max_length=32, primary_key=True)

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Category, self).save(*args, **kwargs)

	class Meta:
		verbose_name_plural = "Categories"

	def __str__(self):
		return self.name

class Article(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	body = models.TextField(max_length=5000)
	author = models.ForeignKey(User)

class Rating(models.Model):
	article = models.ForeignKey(Article)
	user = models.ForeignKey(User)
	rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

	class Meta:
		unique_together = ('article', 'user')

class Comment(models.Model):
	article = models.ForeignKey(Article)
	user = models.ForeignKey(User)
	text = models.TextField(max_length=500)

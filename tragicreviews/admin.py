from django.contrib import admin
from tragicreviews.models import Category, Article, Rating, Comment

class CategoryAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
admin.site.register(Category, CategoryAdmin)

class ArticleAdmin(admin.ModelAdmin):
	list_display = ("title", "body", "author")
admin.site.register(Article, ArticleAdmin)

admin.site.register(Rating)
admin.site.register(Comment)

from django.contrib import admin
from tragicreviews.models import UserProfile, Subject, Article, Rating, Comment

admin.site.register(UserProfile)

class SubjectAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}
admin.site.register(Subject, SubjectAdmin)

class ArticleAdmin(admin.ModelAdmin):
	list_display = ("title", "body", "author")
admin.site.register(Article, ArticleAdmin)

admin.site.register(Rating)
admin.site.register(Comment)

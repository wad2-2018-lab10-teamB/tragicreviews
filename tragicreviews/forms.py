from django import forms
from django.contrib.auth.models import Group
from tragicreviews.models import Subject, Article, Comment
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail


class UserRegistrationForm(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):
    image = forms.ImageField(required=False)  # temp
    majors = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    field_order = ['username', 'email', 'password1', 'password2', 'majors', 'image', 'group', 'tos']


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ("name", )
        help_texts = {"name": "Please enter a subject name"}


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "body")
        help_texts = {
            "title": "Please choose a title for your article",
            "body": "Please include the body of your article"
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text", )
        help_texts = {"text": "Please enter your comment"}

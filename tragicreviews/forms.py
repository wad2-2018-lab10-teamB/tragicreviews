from django import forms
from django.contrib.auth.models import Group
from tragicreviews.models import Subject, Article, Comment, UserLevelField
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail


class UserRegistrationForm(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):

    def get_choices(lst):
        choices = [('', '-----------'),]
        for i in lst:
            choice = (i, i)
            choices.append(choice)
        return choices

    image = forms.ImageField(required=False)  # temp
    majors = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),
                                            widget=forms.CheckboxSelectMultiple, required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    # level will think about it later
    student_levels = get_choices(UserLevelField.student_levels)
    staff_levels = get_choices(UserLevelField.staff_levels)
    student_level = forms.ChoiceField(required=False, widget=forms.Select, choices=student_levels)
    staff_level = forms.ChoiceField(required=False, widget=forms.Select, choices=staff_levels)

    field_order = ['username', 'email', 'password1', 'password2',
                   'group', 'majors', 'student_level', 'staff_level', 'image', 'tos']


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

from django import forms
from django.contrib.auth.models import Group
from tragicreviews.models import Subject, Article, Comment, Rating, UserLevelField, UserProfile
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail


def get_choices(lst):
    choices = [('', '-----------'), ]
    for i in lst:
        choice = (i, i)
        choices.append(choice)
    return choices


def get_update_choices(lst):
    choices = [('', '-----------'), ('clear', 'Clear')]
    for i in lst:
        choice = (i, i)
        choices.append(choice)
    return choices

class UserRegistrationForm(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):

    image = forms.ImageField(required=False)
    majors = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),
                                            widget=forms.CheckboxSelectMultiple, required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)
    student_levels = get_choices(UserLevelField.student_levels)
    staff_levels = get_choices(UserLevelField.staff_levels)
    student_level = forms.ChoiceField(required=False, widget=forms.Select, choices=student_levels)
    staff_level = forms.ChoiceField(required=False, widget=forms.Select, choices=staff_levels)

    field_order = ['username', 'email', 'password1', 'password2',
                   'group', 'majors', 'student_level', 'staff_level', 'image', 'tos']


class UpdateStudentProfileForm(forms.ModelForm):
    # currently we do not allow user to update their email
    image = forms.ImageField(required=False)
    majors = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),
                                            widget=forms.CheckboxSelectMultiple, required=False)
    student_levels = get_update_choices(UserLevelField.student_levels)
    student_level = forms.ChoiceField(required=False, widget=forms.Select, choices=student_levels)

    class Meta:
        model = UserProfile
        exclude = ('user', 'level')


class UpdateStaffProfileForm(forms.ModelForm):
    # currently we do not allow user to update their email
    image = forms.ImageField(required=False)
    majors = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(),
                                            widget=forms.CheckboxSelectMultiple, required=False)
    staff_levels = get_update_choices(UserLevelField.staff_levels)
    staff_level = forms.ChoiceField(required=False, widget=forms.Select, choices=staff_levels)

    class Meta:
        model = UserProfile
        exclude = ('user', 'image', 'majors', 'level')


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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs["rows"] = 4
        
    class Meta:
        model = Comment
        fields = ("text", )
        help_texts = {"text": "Please enter your comment"}


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ("rating", )
        help_texts = {"rating": "Please enter your rating (1-5)"}

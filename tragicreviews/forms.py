from django import forms
from django.contrib.auth.models import Group
from tragicreviews.models import Subject
from registration.forms import RegistrationFormTermsOfService, RegistrationFormUniqueEmail


class UserRegistrationForm(RegistrationFormUniqueEmail, RegistrationFormTermsOfService):
    image = forms.ImageField(required=True)  # temp
    majors = forms.ModelMultipleChoiceField(queryset=Subject.objects.all(), required=True)
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=True)

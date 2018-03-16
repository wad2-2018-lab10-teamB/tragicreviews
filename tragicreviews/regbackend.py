from registration.backends.simple.views import RegistrationView
from tragicreviews.models import UserProfile
from django.contrib.auth.models import Group
from tragicreviews.forms import UserRegistrationForm


class MyRegistrationView(RegistrationView):  # RegistrationView - a subclass of FormView
    form_class = UserRegistrationForm
    success_url = '/accounts/register/'

    def register(self, form):
        user_profile = UserProfile.objects.create_user(form.cleaned_data['username'])
        user_profile.user.email = form.cleaned_data['email']
        user_profile.user.set_password(form.cleaned_data['password1'])
        user_profile.user.groups.add(Group.objects.get(name=form.cleaned_data['group']))

        print(form.cleaned_data['majors'])
        user_profile.majors = form.cleaned_data['majors']
        print(user_profile.majors)  # tragicreviews.Subject.None

        user_profile.image = form.cleaned_data['image']
        user_profile.user.save()
        user_profile.save()
        return user_profile.user

    def get_success_url(self, user):
        return self.success_url

from registration.backends.simple.views import RegistrationView
from tragicreviews.models import UserProfile, Subject
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

        # Adding majors
        print(form.cleaned_data['majors'])
        for major in form.cleaned_data['majors']:
            print(major)
            major.save()
            user_profile.majors.add(major)
        print(user_profile.majors.all())
        # Setting profile image
        if 'image' in form.cleaned_data:
            print("image found")
            user_profile.image = form.cleaned_data['image']
        user_profile.user.save()
        user_profile.save()
        return user_profile.user

    def get_success_url(self, user):
        return self.success_url

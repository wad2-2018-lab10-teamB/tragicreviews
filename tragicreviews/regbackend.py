from registration.backends.simple.views import RegistrationView
from tragicreviews.models import UserProfile, Subject
from django.contrib.auth.models import Group
from tragicreviews.forms import UserRegistrationForm
from django.shortcuts import render
import os


class MyRegistrationView(RegistrationView):  # RegistrationView - a subclass of FormView
    form_class = UserRegistrationForm
    success_url = '/tragicreviews/'

    def register(self, form):
        data = form.cleaned_data
        username = data['username']
        email = data['email']
        password = data['password1']
        group = Group.objects.get(name=data['group'])
        majors = data['majors']
        script_dir = os.path.dirname(__file__)
        default_img = os.path.join(script_dir, '../media/profile_images/default_avatar.jpg')
        image = default_img
        if 'image' in data and data['image'] is not None:
            print("image found")
            print(data['image'])
            image = data['image']

        user_profile = UserProfile.objects.create_user(username)
        user_profile.user.email = email
        user_profile.user.set_password(password)
        user_profile.user.groups.add(group)
        '''
        user_profile = UserProfile.objects.create_user(form.cleaned_data['username'])
        user_profile.user.email = form.cleaned_data['email']
        user_profile.user.set_password(form.cleaned_data['password1'])
        user_profile.user.groups.add(Group.objects.get(name=form.cleaned_data['group']))
        '''
        # Adding majors
        print(form.cleaned_data['majors'])
        for major in majors:
            print(major)
            major.save()
            user_profile.majors.add(major)
        print(user_profile.majors.all())
        # Setting profile image
        user_profile.image = image
        user_profile.user.save()
        user_profile.save()
        return user_profile.user

    def get_success_url(self, user):
        return self.success_url


# for testing, will be removed later
def index(request):
    response = render(request, 'tragicreviews/index.html')
    return response

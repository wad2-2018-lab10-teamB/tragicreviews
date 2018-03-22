from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from tragicreviews.models import UserProfile
from django.contrib.auth.models import Group
from tragicreviews.forms import UserRegistrationForm, UpdateStudentProfileForm, UpdateStaffProfileForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
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
        default_img = 'profile_images/default_avatar.jpg'
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
        # Current set level None

        user_profile.level = None
        if (group.name == 'student'):
            level = data['student_level']
        else:
            level = data['staff_level']
        print(level)
        if (level != ''):
            user_profile.level = level
        # Setting profile image
        user_profile.image = image
        user_profile.user.save()
        user_profile.save()
        return user_profile.user

    def get_success_url(self, user):
        return self.success_url


@login_required
def update_profile(request):
    context_dict = {}

    if request.user.groups.filter(name='student').exists():
        form = UpdateStudentProfileForm()
    else:
        form = UpdateStaffProfileForm()
    if request.method == 'POST':
        if request.user.groups.filter(name='student').exists():
            form = UpdateStudentProfileForm(request.POST)
        else:
            form = UpdateStaffProfileForm(request.POST)
        if form.is_valid():
            user_pf = UserProfile.objects.get(user=request.user)
            if 'image' in request.FILES:
                user_pf.image = request.FILES['image']
            if form.cleaned_data['majors'] is not None:
                user_pf.majors = form.cleaned_data['majors']
            if isinstance(form, UpdateStudentProfileForm):
                new_level = form.cleaned_data['student_level']
            else:
                new_level = form.cleaned_data['staff_level']
            if new_level == 'clear':
                user_pf.level = None
            elif new_level == '':
                pass
            else:
                user_pf.level = new_level
            user_pf.save()
            return HttpResponseRedirect('/tragicreviews/')  # direct user to index page
        else:
            print(form.errors)
    # handle bad forms
    context_dict['form'] = form
    return render(request, 'tragicreviews/update_profile_form.html', context_dict)


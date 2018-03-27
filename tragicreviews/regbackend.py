from registration.backends.simple.views import RegistrationView
from django.contrib.auth.decorators import login_required
from tragicreviews.models import UserProfile
from django.contrib.auth.models import Group, User
from tragicreviews.forms import UserRegistrationForm, UpdateStudentProfileForm, UpdateStaffProfileForm, DeleteUserAccountForm
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.core.urlresolvers import reverse


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

        # Adding majors
        print(form.cleaned_data['majors'])
        for major in majors:
            print(major)
            major.save()
            user_profile.majors.add(major)
        print(user_profile.majors.all())

        # default set level None
        user_profile.level = None
        if group.name == 'student':
            level = data['student_level']
        else:
            level = data['staff_level']
        print(level)
        if level != '':
            user_profile.level = level

        # Setting profile image
        user_profile.image = image
        user_profile.user.save()
        user_profile.save()

        # Auto login
        login(self.request, user_profile.user)
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
            if len(form.cleaned_data['majors']) > 0:
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
            return HttpResponseRedirect(reverse('index'))  # redirect user to index page
        else:
            print(form.errors)
    # handle bad forms
    context_dict['form'] = form
    return render(request, 'tragicreviews/update_profile_form.html', context_dict)


# If a user delete the account, all articles, comments and ratings under that account will be deleted
@login_required
def delete_account(request):
    context_dict = {}
    form = DeleteUserAccountForm()
    if request.method == 'POST':
        form = DeleteUserAccountForm(request.POST)
        if form.is_valid():
            target_user = request.user
            if form.cleaned_data['username'] == target_user.get_username():
                if target_user.check_password(form.cleaned_data['password']) and target_user.check_password(form.cleaned_data['password_confirmation']):
                    if form.cleaned_data['email'] == target_user.email:
                        User.objects.get(username=target_user.get_username()).delete()
                        return HttpResponseRedirect(reverse('delete_account_done'))
                    else:
                        context_dict['message'] = "Incorrect email address."
                else:
                    context_dict['message'] = "Incorrect password or incorrect password confirmation."
            else:
                context_dict['message'] = "Incorrect username."
    context_dict['form'] = form
    return render(request, 'tragicreviews/delete_account.html', context_dict)


def delete_account_done(request):
    response = render(request, 'tragicreviews/delete_account_done.html')
    return response

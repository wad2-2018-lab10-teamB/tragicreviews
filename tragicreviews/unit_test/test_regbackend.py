from django.test import TestCase
from django.core.urlresolvers import reverse
from tragicreviews.models import Subject, UserProfile, Article, Rating, Comment
import tragicreviews.unit_test.test_utils as test_utils
from django.contrib.auth.models import User, Group
from tragicreviews.forms import UserRegistrationForm, UpdateStudentProfileForm, UpdateStaffProfileForm, DeleteUserAccountForm

"""
Unit tests for user authentication functionality and forms
"""


class TestRegbackend(TestCase):

    def test_get_user_registeration_form_correct(self):
        response = self.client.get(reverse('registration_register'))
        self.assertTrue(isinstance(response.context['form'], UserRegistrationForm))
        form = UserRegistrationForm()
        self.assertEqual(response.context['form'].as_p(), form.as_p())

    def test_user_registration(self):
        test_utils.create_subject()
        test_utils.create_groups()
        data = {
            'username': 'testuser',
            'email': 'example@example.com',
            'password1': 'something123',
            'password2': 'something123',
            'group': 1,  # 1-student 2-staff
            'majors': Subject.objects.filter(name='foo'),
            'student_level': '',
            'staff_level': '',
            'image': None,
            'tos': True
        }
        # Test valid form
        form = UserRegistrationForm(data=data)
        self.assertTrue(form.is_valid())

        # Test user successful registration
        response = self.client.post(reverse('registration_register'), data=data)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(UserProfile.objects.all().count(), 1)

        # Test redirect to index page after successful registration
        # Success url is set to '/tragicreviews/', which is index page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_handle_bad_registration_form(self):
        test_utils.create_subject()
        test_utils.create_groups()
        data = {
            'username': 'testuser',
            'email': 'example@example.com',
            'password1': 'something123',
            'password2': 'something123',
            'group': 1,
            'majors': Subject.objects.filter(name='foo'),
            'student_level': '',
            'staff_level': '',
            'image': None,
            'tos': True
        }

        # Miss user name
        data1 = data
        data1['username'] = None
        form = UserRegistrationForm(data=data1)
        self.assertFalse(form.is_valid())

        # Incorrect email address
        data1 = data
        data1['email'] = '123abc'
        form = UserRegistrationForm(data=data1)
        self.assertFalse(form.is_valid())

        # Miss password
        data1 = data
        data1['password1'] = None
        form = UserRegistrationForm(data=data1)
        self.assertFalse(form.is_valid())

        # Password not match
        data1 = data
        data1['password2'] = 'something1234'
        form = UserRegistrationForm(data=data1)
        self.assertFalse(form.is_valid())

        # Miss majors
        data1 = data
        data1['majors'] = None
        form = UserRegistrationForm(data=data1)
        self.assertFalse(form.is_valid())

        # Miss Group
        data1 = data
        data1['group'] = 0
        form = UserRegistrationForm(data=data1)
        self.assertFalse(form.is_valid())

    def test_user_login(self):
        test_utils.create_user_profile_for_testing()
        response = self.client.post(reverse('auth_login'), data={'username': 'dummy', 'password': 'test1234'})

        # Test successful login, redirect to correct page
        # In settings.py, LOGIN_REDIRECT_URL = '/'
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')

    def test_user_change_password(self):
        test_utils.create_user_profile_for_testing()
        # User login first
        response = self.client.login(username='dummy', password='test1234')
        self.assertTrue(response)

        response = self.client.post(reverse('auth_password_change'),
                                    data={'old_password': 'test1234', 'new_password1': 'test1235',
                                          'new_password2': 'test1235'})

        # Test password is changed successfully
        user = UserProfile.objects.get_by_username('dummy').user
        self.assertFalse(user.check_password('test1234'))
        self.assertTrue(user.check_password('test1235'))

        # Test redirecting to correct page after changing password
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('auth_password_change_done'))

    def test_student_user_update_profile(self):
        test_utils.create_subject()
        student = test_utils.create_student_user_profile()
        # User login first
        response = self.client.login(username='dummy', password='test1234')
        self.assertTrue(response)

        # Test get correct update profile form
        response = self.client.get(reverse('update_profile'))
        self.assertTrue(isinstance(response.context['form'], UpdateStudentProfileForm))

        data = {'image': None,
                'majors': Subject.objects.filter(name='foo'),
                'student_level': 'Level 1 undergraduate'
                }

        # Test form is valid
        form = UpdateStudentProfileForm(data=data)
        self.assertTrue(form.is_valid())

        # Test update a user profile successfully
        response = self.client.post(reverse('update_profile'), data=data)
        self.assertEqual(UserProfile.objects.get_by_username(student).level, 'Level 1 undergraduate')
        self.assertEqual(UserProfile.objects.get_by_username(student).majors.count(), 1)

        # Test redirecting to index page after updating user profile
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_staff_user_update_profile(self):
        test_utils.create_subject()
        staff = test_utils.create_staff_user_profile()
        # User login first
        response = self.client.login(username='dummy', password='test1234')
        self.assertTrue(response)

        # Test get correct update profile form
        response = self.client.get(reverse('update_profile'))
        self.assertTrue(isinstance(response.context['form'], UpdateStaffProfileForm))

        data = {'image': None,
                'majors': Subject.objects.filter(name='foo'),
                'staff_level': 'Lecturer'
                }

        # Test form is valid
        form = UpdateStaffProfileForm(data=data)
        self.assertTrue(form.is_valid())

        # Test update a user profile successfully
        response = self.client.post(reverse('update_profile'), data=data)
        self.assertEqual(UserProfile.objects.get_by_username(staff).level, 'Lecturer')
        self.assertEqual(UserProfile.objects.get_by_username(staff).majors.count(), 1)

        # Test redirecting to index page after updating user profile
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_user_delete_account(self):
        username = test_utils.create_user_profile_for_testing()
        user_pf = UserProfile.objects.get_by_username(username)
        user = user_pf.user
        # User login first
        response = self.client.login(username=username, password='test1234')
        self.assertTrue(response)

        # Test get correct delete account form
        response = self.client.get(reverse('delete_account'))
        self.assertTrue(isinstance(response.context['form'], DeleteUserAccountForm))

        data = {'username': 'dummy',
                'password': 'test1234',
                'password_confirmation': 'test1234',
                'email': 'test@test.com'
                }

        # Test form is valid
        form = DeleteUserAccountForm(data=data)
        self.assertTrue(form.is_valid())

        # Test delete an account successfully
        response = self.client.post(reverse('delete_account'), data=data)
        self.assertEqual(UserProfile.objects.filter(user=user).count(), 0)
        self.assertEqual(User.objects.filter(username=username).count(), 0)

        # Test all articles, comments and ratings under that account are deleted
        self.assertEqual(Article.objects.filter(author=user_pf).count(), 0)
        self.assertEqual(Rating.objects.filter(user=user_pf).count(), 0)
        self.assertEqual(Comment.objects.filter(user=user_pf).count(), 0)

        # Test redirecting to index page after updating user profile
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('delete_account_done'))

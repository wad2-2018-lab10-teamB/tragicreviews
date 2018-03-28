from django.test import TestCase
from django.core.urlresolvers import reverse
from tragicreviews.models import Article, Comment, Rating, ArticleViews, UserProfile, Subject
import tragicreviews.unit_test.test_utils as test_utils
from tragicreviews.forms import ArticleForm

"""
Unit tests for views and forms which are used by views.
"""


class TestViews(TestCase):
    def test_index(self):
        response = self.client.get(reverse('index'))
        # Test HttpResponse OK
        self.assertEqual(response.status_code, 200)
        # Test no trending articles
        self.assertEqual(len(response.context['trend_articles']), 0)
        # Test no new articles
        self.assertEqual(len(response.context['new_articles']), 0)

    def test_index_with_articles(self):
        test_utils.create_article_views()
        response = self.client.get(reverse('index'))
        self.assertEqual(len(response.context['trend_articles']), 1)
        self.assertEqual(len(response.context['new_articles']), 1)

    def test_category_exist(self):
        test_utils.create_article()  # s = Subject(name="bar")
        response = self.client.get(reverse('category', args=['bar']))
        self.assertEqual(response.context['category'].name, 'bar')
        self.assertEqual(len(response.context['articles']), 1)

    def test_category_not_exist(self):
        response = self.client.get(reverse('category', args=['bar']))
        self.assertEqual(response.status_code, 404)

    def test_article_not_login(self):
        test_utils.create_article_for_testing_article_view()  # s = Subject(name="bar")
        article_object = Article.objects.all()[0]
        article_id = article_object.id
        comment_set = Comment.objects.filter(article=article_object)
        rating_avg = Rating.objects.get_average_rating(article_object)
        views = ArticleViews.objects.get_total_views(article_object)
        response = self.client.get(reverse('article', args=['bar', article_id]))

        # Test correctness of article title, author, body text, category and average rating
        self.assertEqual(response.context['article'].title, article_object.title)
        self.assertEqual(response.context['article'].author, article_object.author)
        self.assertEqual(response.context['article'].body, article_object.body)
        self.assertEqual(response.context['article'].category, article_object.category)
        self.assertEqual(response.context['rating_avg'], rating_avg)

        # Test the number of comments in comment set is correct
        self.assertEqual(len(response.context['comment_set']), len(comment_set))

        # Article views should be increase by 1
        self.assertEqual(response.context['total_views'], (views + 1))
        # Article views in database should also be increased
        self.assertEqual(response.context['total_views'], ArticleViews.objects.get_total_views(article_object))

    def test_add_article(self):
        # User login
        user_pf = test_utils.create_user()
        user_pf.user.set_password('test1234')
        user_pf.user.save()
        user_pf.save()
        response = self.client.login(username='dummy', password='test1234')
        self.assertTrue(response)
        subject = test_utils.create_subject()
        response = self.client.post(reverse('add_article', args=[subject.slug, ]),
                         data={'title': 'My Article', 'body': 'some text'})

        # Test article is added correctly
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.filter(category=subject).count(), 1)
        self.assertEqual(Article.objects.filter(author=user_pf).count(), 1)
        a = Article.objects.get(category=subject)
        # Test correctly redirect to index page after adding article
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('article', args=[a.category, a.id]))

    def test_delete_article(self):
        # Login a user
        username = test_utils.create_user_profile_for_testing()
        response = self.client.login(username='dummy', password='test1234')
        self.assertTrue(response)
        a = Article.objects.filter(author=UserProfile.objects.get_by_username(username))[0]
        response = self.client.get(reverse('delete_article', args=[a.category.slug, a.id]), follow=True)
        self.assertContains(response, 'Are you sure you want to delete')

    def test_edit_article(self):
        # Login a user
        username = test_utils.create_user_profile_for_testing()
        response = self.client.login(username='dummy', password='test1234')
        self.assertTrue(response)
        a = Article.objects.filter(author=UserProfile.objects.get_by_username(username))[0]
        data = {
            'title': a.title + ' new',
            'body': a.body + ' new'
        }

        response = self.client.get(reverse('edit_article', args=[a.category.slug, a.id]))

        # Test original article is in form
        self.assertContains(response, "User Article")
        self.assertContains(response, "User article content")
        response = self.client.post(reverse('edit_article', args=[a.category.slug, a.id]),
                                    data=data)
        # Test redirect to article page after edit
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('article', args=[a.category, a.id]))

        # Test successfully edit article
        new_a = Article.objects.filter(author=UserProfile.objects.get_by_username(username))[0]
        self.assertEquals(new_a.title, data['title'])
        self.assertEquals(new_a.body, data['body'])

    def test_profile(self):
        user_pf_id = test_utils.create_user_profile_for_testing()  # user_pf_id is username
        user_pf = UserProfile.objects.get_by_username(user_pf_id)
        response = self.client.get(reverse('profile', args=[user_pf_id, ]))
        # Test correctness of getting user profile
        self.assertEqual(response.context["user_profile"], user_pf)

    def test_profile_reviews(self):
        user_pf_id = test_utils.create_user_profile_for_testing()  # same - user_pf_id is username
        user_pf = UserProfile.objects.get_by_username(user_pf_id)
        response = self.client.get(reverse('profile_reviews', args=[user_pf_id, ]))
        # Test the number of ratings is correct
        self.assertEqual(response.context['ratings'].count(), Rating.objects.filter(user=user_pf).count())

    def test_profile_uploads(self):
        user_pf_id = test_utils.create_user_profile_for_testing()  # same - user_pf_id is username
        user_pf = UserProfile.objects.get_by_username(user_pf_id)
        response = self.client.get(reverse('profile_uploads', args=[user_pf_id, ]))
        # Test the number of articles is correct
        self.assertEqual(response.context['user_articles'].count(), Article.objects.filter(author=user_pf).count())

    def test_article_with_user_login(self):
        # User login
        user_pf = test_utils.create_user()
        user_pf.user.set_password('test1234')
        user_pf.user.save()
        user_pf.save()
        response = self.client.login(username='dummy', password='test1234')
        self.assertTrue(response)

        test_utils.create_article_for_testing_article_view()  # s = Subject(name="bar")
        article_object = Article.objects.all()[0]
        article_id = article_object.id

        # Test rating an article
        self.client.post(reverse('article', args=['bar', article_id]), data={'ratingbtn': 'Submit', 'rev-rating': 1})
        rating_response = self.client.get(reverse('article', args=['bar', article_id]))
        self.assertEqual(rating_response.context['rating_avg'], (1+4)/2.0)
        self.assertEqual(article_object.rating_set.count(), 2)

        # Test a user can rate an article only once
        self.client.post(reverse('article', args=['bar', article_id]), data={'ratingbtn': 'Submit', 'rev-rating': 2})
        rating_response = self.client.get(reverse('article', args=['bar', article_id]))
        self.assertEqual(rating_response.context['rating_avg'], (2 + 4) / 2.0)
        self.assertEqual(article_object.rating_set.count(), 2)

        # Test adding a comment to an article
        self.client.post(reverse('article', args=['bar', article_id]),
                         data={'com-text': 'Some new comments', 'commentbtn': 'Submit'})
        response = self.client.get(reverse('article', args=['bar', article_id]))
        self.assertEqual(response.context['comment_set'].count(), 2)
        self.assertEqual(Comment.objects.filter(article=article_object).count(), 2)

        # Test a user can post more that one comments to an article
        self.client.post(reverse('article', args=['bar', article_id]),
                         data={'com-text': 'Some new comments again', 'commentbtn': 'Submit'})
        response = self.client.get(reverse('article', args=['bar', article_id]))
        self.assertEqual(response.context['comment_set'].count(), 3)
        self.assertEqual(Comment.objects.filter(article=article_object).count(), 3)

    def test_add_category(self):
        # Login a staff account
        staff = test_utils.create_staff_user_profile()
        response = self.client.login(username=staff, password='test1234')
        self.assertTrue(response)

        # Test add a category
        response = self.client.post(reverse('add_category'), data={'name': 'New Category'})
        self.assertEqual(Subject.objects.filter(name='New Category').count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_add_category_forbidden(self):
        # Login a student account
        student = test_utils.create_student_user_profile()
        response = self.client.login(username=student, password='test1234')
        self.assertTrue(response)

        # Test add a category fail and get forbidden code 403
        response = self.client.post(reverse('add_category'), data={'name': 'New Category'})
        self.assertEqual(Subject.objects.filter(name='New Category').count(), 0)
        self.assertEqual(response.status_code, 403)

    def test_delete_category(self):
        # Login a staff account
        staff = test_utils.create_staff_user_profile()
        test_utils.create_subject()
        response = self.client.login(username=staff, password='test1234')
        self.assertTrue(response)

        # Test delete a category
        response = self.client.post(reverse('delete_category', args=['foo', ]), data={'confirm_delete': True})
        self.assertEqual(Subject.objects.all().count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_delete_category_forbidden(self):
        # Login a student account
        student = test_utils.create_student_user_profile()
        test_utils.create_subject()
        response = self.client.login(username=student, password='test1234')
        self.assertTrue(response)

        # Test delete a category fail and get forbidden code 403
        response = self.client.post(reverse('delete_category', args=['foo', ]), data={'confirm_delete': True})
        self.assertEqual(Subject.objects.filter(name='foo').count(), 1)
        self.assertEqual(response.status_code, 403)

    def test_update_category(self):
        # Login a staff account
        staff = test_utils.create_staff_user_profile()
        test_utils.create_article()
        response = self.client.login(username=staff, password='test1234')
        self.assertTrue(response)

        # Test delete a category
        response = self.client.post(reverse('update_category', args=['bar', ]), data={'name': 'foo'})
        self.assertEqual(Subject.objects.filter(name='bar').count(), 0)
        self.assertEqual(Subject.objects.filter(name='foo').count(), 1)
        self.assertEqual(Article.objects.filter(category='foo').count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))

    def test_update_category_forbidden(self):
        # Login a student account
        student = test_utils.create_student_user_profile()
        test_utils.create_article()
        response = self.client.login(username=student, password='test1234')
        self.assertTrue(response)

        # Test update a category fail and get forbidden code 403
        response = self.client.post(reverse('delete_category', args=['bar', ]), data={'name': 'foo'})
        self.assertEqual(Subject.objects.filter(name='foo').count(), 0)
        self.assertEqual(response.status_code, 403)

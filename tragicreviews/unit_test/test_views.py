from django.test import TestCase
from django.core.urlresolvers import reverse
from tragicreviews.models import Article, Comment, Rating, ArticleViews, UserProfile
import tragicreviews.unit_test.test_utils as test_utils


class TestViews(TestCase):
    def test_index(self):
        response = self.client.get(reverse('index'))
        # Test HttpResponse OK
        self.assertEqual(response.status_code, 200)
        # Test no user login
        self.assertEqual(response.context['username'].get_queryset().count(), 0)
        # Test no trending articles
        self.assertEqual(len(response.context['trend_articles']), 0)
        # Test no new articles
        self.assertEqual(len(response.context['new_articles']), 0)

    def test_index_with_user_login(self):
        user_pf = test_utils.create_user()
        user_pf.user.set_password('test1234')
        user_pf.user.save()
        user_pf.save()
        response = self.client.login(username='dummy', password='test1234')
        # Test user login successful
        self.assertTrue(response)
        # Test the number of login user is correct
        response = self.client.get(reverse('index'))
        self.assertEqual(response.context['username'].get_queryset().count(), 1)

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
        self.assertIsNone(response.context['category'])
        self.assertIsNone(response.context['articles'])

    def test_article_not_login(self):
        test_utils.create_article_for_testing_article_view()  # s = Subject(name="bar")
        article_object = Article.objects.all()[0]
        article_id = article_object.id
        comment_set = Comment.objects.filter(article=article_object)
        rating_avg = Rating.objects.get_average_rating(article_object)
        views = ArticleViews.objects.get_total_views(article_object)
        response = self.client.get(reverse('article', args=['bar', article_id]))

        # Test correctness of article title, author, body text, category and average rating
        self.assertEqual(response.context['title'], article_object.title)
        self.assertEqual(response.context['author'], article_object.author)
        self.assertEqual(response.context['text'], article_object.body)
        self.assertEqual(response.context['category'], article_object.category)
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
        self.client.post(reverse('add_article', args=[subject.slug, ]),
                         data={'title': 'My Article', 'body': 'some text'})
        # Test article is added correctly
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(Article.objects.filter(category=subject).count(), 1)
        self.assertEqual(Article.objects.filter(author=user_pf).count(), 1)

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

    # Fix test post rating and comment later
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
        comment_set = Comment.objects.filter(article=article_object)
        rating_avg = Rating.objects.get_average_rating(article_object)
        views = ArticleViews.objects.get_total_views(article_object)
        rating_response = self.client.post(reverse('article', args=['bar', article_id]),
                         data={'rating': 1, 'ratingbtn': 'ratingbtn'})
        print(rating_response)

        self.client.post(reverse('article', args=['bar', article_id]),
                         data={'text': 'Some new comments', 'commentbtn': 'commentbtn'},)
        response = self.client.get(reverse('article', args=['bar', article_id]))
        print(Comment.objects.filter(article=article_object))
        print(Rating.objects.get_average_rating(article_object))


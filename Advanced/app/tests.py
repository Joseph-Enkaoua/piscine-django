from django.test import TestCase, Client
from django.urls import reverse
from app.models import *


class AuthenticatedViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = Client()

    def test_favorites_view_requires_login(self):
        response = self.client.get(reverse('app:favorites'))
        self.assertNotEqual(response.status_code, 200)

    def test_publications_view_requires_login(self):
        response = self.client.get(reverse('app:publications'))
        self.assertNotEqual(response.status_code, 200)

    def test_publish_view_requires_login(self):
        response = self.client.get(reverse('app:publish'))
        self.assertNotEqual(response.status_code, 200)

    def test_favorites_view_served_when_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('app:favorites'))
        self.assertEqual(response.status_code, 200)
    
    def test_publications_view_served_when_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('app:publications'))
        self.assertEqual(response.status_code, 200)
    
    def test_publish_view_served_when_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('app:publish'))
        self.assertEqual(response.status_code, 200)


class RegistrationAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client = Client()
        self.client.login(username='testuser', password='testpassword')

    def test_registered_user_cannot_access_registration(self):
        response = self.client.get(reverse('app:register'), follow=True)
        self.assertRedirects(response, reverse('app:articles'))


class FavouriteTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.article = Article.objects.create(
            title='Test article',
            author=self.user,
            synopsis='Test synopsis',
            content='Content'
        )
        self.client.get(reverse("app:article_detail", args=[self.article.id]))

    def test_article_detail_renders_add_to_favorite_form(self):
        response = self.client.get(reverse("app:article_detail", args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "article_detail.html")
        self.assertContains(
            response, 'action="{0}"'.format(reverse("app:add_to_favorite", args=[self.article.id]))
        )

    def test_add_to_favorites_submission(self):
        """Test submitting the add-to-favorites form."""
        self.client.post(reverse("app:add_to_favorite", args=[self.article.id]), follow=True)
        self.assertEqual(
            UserFavoriteArticle.objects.filter(user=self.user, article=self.article).count(),
            1,
        )

    def test_cannot_add_duplicate_favorite_via_view(self):
        """Test that the view handles duplicate favorites gracefully."""
        # First attempt to add to favorites
        self.client.post(reverse("app:add_to_favorite", args=[self.article.id]))
        self.assertEqual(UserFavoriteArticle.objects.filter(user=self.user, article=self.article).count(), 1)

        # Second attempt to add the same article
        self.client.post(reverse("app:add_to_favorite", args=[self.article.id]), follow=True)

        # Check that the duplicate favorite was not created
        self.assertEqual(UserFavoriteArticle.objects.filter(user=self.user, article=self.article).count(), 1)

from django.contrib import admin
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from .admin import ArticleAdmin
from .models import Advertisement, Article, ArticleDetailAdvertisement

class ArticleDetailAdvertisementTests(TestCase):
	def test_article_detail_ads_are_independent_of_home_ads(self):
		Advertisement.objects.create(title="Home campaign")
		ArticleDetailAdvertisement.objects.create(slot=1, title="Article campaign")

		self.assertEqual(Advertisement.objects.count(), 1)
		self.assertEqual(ArticleDetailAdvertisement.objects.count(), 1)
		self.assertEqual(ArticleDetailAdvertisement.objects.get().slot, 1)

class ArticlePublicationDateAdminTests(TestCase):
	def test_publication_date_is_editable_in_admin_form(self):
		request = RequestFactory().get("/admin/main/article/")
		request.user = AnonymousUser()
		form_class = ArticleAdmin(Article, admin.site).get_form(request)

		self.assertIn("created_at", form_class.base_fields)

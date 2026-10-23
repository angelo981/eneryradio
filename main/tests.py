from django.contrib import admin
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, TestCase
from .admin import ArticleAdmin
from .models import Advertisement, Article, ArticleDetailAdvertisement, Blog

class BlogDetailTests(TestCase):
	def test_blog_card_detail_page_shows_full_blog(self):
		full_description = "Full description " * 40 + "This is the complete final sentence."
		blog = Blog.objects.create(
			title="A complete story",
			Summary=full_description,
			content="<p>The complete blog content.</p>",
		)

		response = self.client.get(f"/blogs/{blog.pk}/")

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "This is the complete final sentence.")
		self.assertContains(response, "The complete blog content.")

	def test_blog_listing_links_to_blog_detail(self):
		original_summary = "First line exactly as written.\nSecond line keeps its Capitalization."
		blog = Blog.objects.create(
			title="Clickable story",
			Summary=original_summary,
			content="<p>Extra words that are not part of the description.</p>",
		)

		response = self.client.get("/blogs")

		self.assertContains(response, f'href="/blogs/{blog.pk}/"')
		self.assertContains(response, f'data-blog-template="journal-story-{blog.pk}"')
		self.assertContains(response, '<dialog class="journal-dialog"')
		self.assertContains(response, original_summary)
		self.assertNotContains(response, "Extra words that are not part of the description.")

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

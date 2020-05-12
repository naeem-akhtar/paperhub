from django.test import SimpleTestCase
from django.urls import reverse, resolve
from posts.views import (
	PostList, PostDetail, UserPostList, PostCreate, PostUpdate, PostDelete, PostBookmark, UserBookmarkPostList
)
from users.models import User


class TestUrls(SimpleTestCase):
	def setUp(self):
		pass

	def test_all_post_list_url_resolved(self):
		url = reverse('home')
		self.assertEquals(resolve(url).func.view_class, PostList)

	def test_bookmark_url_resolvd(self):
		url = reverse('bookmark')
		self.assertEquals(resolve(url).func.view_class, PostBookmark)

	def test_user_bookmark_list_url_resolved(self):
		url = reverse('user-bookmarked-posts', args=['asdad'])
		self.assertEquals(resolve(url).func.view_class, UserBookmarkPostList)

	def test_user_post_list_url_resolved(self):
		url = reverse('user-posts', args=['jkabkc'])
		self.assertEquals(resolve(url).func.view_class, UserPostList)

	def test_post_create_url_resolved(self):
		url = reverse('post-create')
		self.assertEquals(resolve(url).func.view_class, PostCreate)

	def test_post_detail_url_resolved(self):
		url = reverse('post-detail', args=[56541316313])
		self.assertEquals(resolve(url).func.view_class, PostDetail)

	def test_post_update_url_resolved(self):
		url = reverse('post-update', args=[0])
		self.assertEquals(resolve(url).func.view_class, PostUpdate)

	def test_post_delete_url_resolved(self):
		url = reverse('post-delete', args=[11])
		self.assertEquals(resolve(url).func.view_class, PostDelete)
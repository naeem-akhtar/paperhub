from django.test import SimpleTestCase
from django.urls import reverse, resolve
from users.views import (
 UserProfile, register, validate_username, confirm_email, profile_update,
 FollowUser, UserFollower, UserFollowing
)


class TestUrls(SimpleTestCase):
	def test_validate_username_url_resolved(self):
		url = reverse('validate_username')
		self.assertEquals(resolve(url).func, validate_username)

	def test_follow_unfollow_url_resolved(self):
		url = reverse('follow_unfollow')
		self.assertEquals(resolve(url).func, FollowUser)	

	def test_follower_user_url_resolved(self):
		url = reverse('followers', args=['sada'])
		self.assertEquals(resolve(url).func.view_class, UserFollower)

	def test_following_user_url_resolved(self):
		url = reverse('following', args=['sada'])
		self.assertEquals(resolve(url).func.view_class, UserFollowing)

	def test_profile_update_url_resolved(self):
		url = reverse('profile-update')
		self.assertEquals(resolve(url).func, profile_update)

	def test_profile_detail_url_resolved(self):
		url = reverse('profile', args=['sdjjasjka'])
		self.assertEquals(resolve(url).func.view_class, UserProfile)

	def test_register_url_resolved(self):
		url = reverse('register')
		self.assertEquals(resolve(url).func, register)

	# def test_confirm_email_url_resolved(self):
	# 	url = reverse('activate', args=['asxsad', 'sadasd'])
	# 	self.assertEquals(resolve(url).func, confirm_email)
	


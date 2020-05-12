from django.test import TestCase, Client
from django.urls import reverse
from users.models import User
from posts.models import Post, Bookmark
from moto import mock_s3
import boto3

@mock_s3
class TestViews(TestCase):
	def setUp(self):
		self.client = Client()
		self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		self.other_user = User.objects.create_user('johnwick', 'lennon@gmail.com', 'johnpassword')
		# self.post = Post.objects.create('')

	def test_post_list_GET(self):
		response = self.client.get(reverse('home'))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'posts/home.html')

	def test_post_detail_GET(self):
		response = self.client.get(reverse('post-detail', args=[2]))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'posts/post_detail.html')

	# def test_post_update_GET(self):
	# 	response = self.client.get(reverse('post-detail', {'post_id' : 1}))	
	# 	self.assertEquals(response.status_code, 200)
	# 	self.assertTemplateUsed(response, 'posts/post_form.html')	
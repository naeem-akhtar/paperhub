from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, Profile, UserConnection
from moto import mock_s3
import boto3

@mock_s3
class TestViews(TestCase):
	def setUp(self):
		self.client = Client()
		self.register_url = reverse('register')
		self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
		self.other_user = User.objects.create_user('johnwick', 'lennon@gmail.com', 'johnpassword')

	# registration form
	def test_register_GET(self):
		response = self.client.get(self.register_url)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'users/register.html')

	def test_register_POST(self):
		response = self.client.post(self.register_url, {
				'username' : 'thanos',
				'email' : 'thanos@gmail.com',
				'password' : 'Naeem@12345',
			})
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'users/register.html')
	
	# check username already exixts
	def test_validate_username_GET(self):
		response = self.client.get(reverse('validate_username'))
		self.assertEquals(response.status_code, 200)

	# profile update
	def test_profile_update_GET(self):
		self.client.login(username='john', password='johnpassword')
		response = self.client.get(reverse('profile-update'))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'users/profile_form.html')

	# def test_profile_update_POST(self):
	# 	self.client.login(username='john', password='johnpassword')
	# 	response = self.client.post(reverse('profile-update'), {

	# 		})
	# 	self.assertEquals(response.status_code, 200)
	# 	self.assertTemplateUsed(response, 'users/profile_form.html')

	# toggle follow - unfollow
	def test_follow_unfollow_GET(self):
		self.client.login(username='john', password='johnpassword')
		response = self.client.get(reverse('follow_unfollow'), {
				'username' : 'johnwick',
				'operation' : 'check'
			})
		self.assertEquals(response.status_code, 200)

	# list of followers
	def test_user_folower_GET(self):
		self.client.login(username='john', password='johnpassword')
		response = self.client.get(reverse('followers', args=['jacnk']))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'users/user_list.html')
	
	# list of following
	def test_user_folowing_GET(self):
		self.client.login(username='john', password='johnpassword')
		response = self.client.get(reverse('following', args=['asda']))
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'users/user_list.html')
	
	

from django.test import TestCase, Client

class TestModels(TestCase):
	def setUp(self):
		self.user = User.objects.create(
			username = 'john',
			email = 'john@killstreak.com',
			password = 'Naeem@12345'
		)
		# self.profile = Profile.objects.create(

		# )
	
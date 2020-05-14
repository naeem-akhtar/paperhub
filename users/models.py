from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.files import File
from io import BytesIO
from PIL import Image
from django.core.exceptions import ValidationError

# helping functions and classes
def validate_DOB(value):
	if False:
		raise ValidationError(f'%s is not a valid date of birth.' % value)

def crop_image(model_image, side=None):
	image = Image.open(model_image)
	if image.mode != 'RGB':
		image = image.convert('RGB')
	# new side, min of width and height
	side = min(image.size)
	dimensions  = 0, 0, side, side
	croped = image.crop(dimensions)
	return croped	

def compress_image(croped, name, quality=60):
	image_io = BytesIO()
	croped.save(image_io, 'JPEG', quality=quality)
	final_image = File(image_io, name=name)
	return final_image

def create_thumbnail(croped, name, size=100):
	image_io = BytesIO()
	size = min(size, min(croped.size))
	croped.thumbnail((size, size))	# making thumbnail
	croped.save(image_io, 'JPEG')
	final_image = File(image_io, name=name)
	return final_image


# Create your models here.
class User(AbstractUser):
	class Meta:
		permissions = [
			('verified', 'User verified'),
		]


class Profile(models.Model):
	GENDER = (('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other'), ('NOT_SPECIFIED', 'Not Specified'))

	user  = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField('User Avatar', upload_to='profile_pictures', default='profile_pictures/default_thumbnail.jpg')
	thumbnail = models.ImageField('User Avatar', upload_to='profile_pictures/thumbs', default='profile_pictures/default_thumbnail.jpg')
	dob = models.DateField('DOB', null=True, blank=True, validators=[validate_DOB])
	gender = models.CharField('Gender', max_length=15, choices=GENDER, default='NOT_SPECIFIED')
	bio = models.TextField('Bio', max_length=500, blank=True)

	def __str__(self):
		return f'{self.user.username} Profile'

	def save(self, *args, **kwargs):
		# crop biggest square from image and compress it a little.
		croped_image = crop_image(self.image)	
		self.image = compress_image(croped_image, self.user.username + '_avatar.jpg')
		# create a seperate thumbnail
		self.thumbnail = create_thumbnail(croped_image, self.user.username + '_thumb.jpg')
		# save / update the Profile
		super().save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('profile/<username>', kwargs={'username':self.user.username})


class UserConnection(models.Model):
	# The person who is following will be follower
	follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
	# The person who is being followed will be following
	following = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
	timestamp = models.DateTimeField(default = timezone.now)

	class Meta:
		ordering = ['timestamp']
		unique_together = ('follower', 'following')

	def __str__(self):
		return '%s follows %s' % (self.follower, self.following)
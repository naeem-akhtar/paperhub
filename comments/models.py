from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model, get_user
from mptt.models import MPTTModel, TreeForeignKey
from posts.models import Post

User = get_user_model()

# Create your models here.
class Comment(MPTTModel):
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
	reply_to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='replyers')
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	comment = models.TextField('comment', max_length=1000)
	created = models.DateTimeField('created', default = timezone.now)

	class MPTTMeta:
		order_insertion_by = ['created']

	def __str__(self):
		return f'{self.user.username}' + ' : ' + f'{self.comment[:20]}'

	# def get_absolute_url(self):
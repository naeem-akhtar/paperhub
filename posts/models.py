from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, get_user
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase, Tag


User = get_user_model()

def validate_document_size(doc, limit_kb=5000):
	file_size = doc.file.size
	if file_size > limit_kb*1024:
		raise ValidationError('Max allowd file size is %s KB' % limit_kb)


class PostTag(TaggedItemBase):
	content_object = models.ForeignKey('Post', on_delete=models.CASCADE)


# Create your models here.
class Post(models.Model, HitCountMixin):
	author = models.ForeignKey(User, related_name='authors', on_delete=models.CASCADE)
	title = models.CharField('Post Title', max_length = 150)
	description = models.TextField('Description', max_length=1000, blank = True)
	date_posted = models.DateTimeField('Date posted', default = timezone.now)
	date_modifed = models.DateTimeField('Date last modified', default = timezone.now)
	document = models.FileField('Document of Post', upload_to='documents', \
	 validators=[FileExtensionValidator(allowed_extensions = ['pdf', 'docx']), validate_document_size] \
	)
	hit_count_generic = GenericRelation(
    HitCount,
    object_id_field='object_pk',
    related_query_name='hit_count_generic_relation'
  )
	tags = TaggableManager(through = PostTag, blank = True)
	# add { likes, dislikes, bookmark, hash-tags } in future

	def __str__(self):
		return f'{self.title}'

	@property
	def bookmark_user_id(self):
		bookmarks = self.bookmark_set.all()
		# return [username[0] for username in bookmarks.values_list('user__username')]
		return [user_id[0] for user_id in bookmarks.values_list('user')]

	@property
	def views(self):
		return self.hit_count.hits

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk':self.pk})


class Bookmark(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	timestamp = models.DateTimeField('Bookmark time', default=timezone.now)

	class Meta:
		unique_together = ('user', 'post')

	def __str__(self):
		return f'post (id = {self.post.id}) bookmarked by {self.user.username}'

	def get_absolute_url(self):
		return reverse('bookmark', kwargs={'pk':self.post.pk})


class PostTagExtended(models.Model):
	tag = models.OneToOneField(Tag, on_delete = models.CASCADE)
	# creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	created = models.DateTimeField(default = timezone.now)
	count = models.PositiveIntegerField('tag_count', default = 0)	# number of times tag is used
	followers = models.ManyToManyField(User, related_name='tags_following')

	def __str__(self):
		return f'{self.count}'

	def get_absolute_url(self):
		return reverse('tag/<slug:tag_slug>', kwargs={'tag_slug':self.tag.slug})
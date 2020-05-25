from django.db.models.signals import post_save, post_delete
# from django.contrib.auth import get_user_model
from django.dispatch import receiver
from taggit.models import Tag
from .models import PostTag, PostTagExtended

# print('signals imported')
# User = get_user_model()

# A new tag is saved, create extended part
@receiver(post_save, sender = Tag)
def create_extended_tag(sender, instance, created, **kwargs):
	if created:
		# print('profile is being created')
		PostTagExtended.objects.create(tag = instance)


# new extended part is created save it.
# @receiver(post_save, sender = Tag)
# def save_extended_tag(sender, instance, created, **kwargs):
# 	# print('profile is saved')
# 	instance.PostTagExtended.save()

@receiver(post_save, sender = PostTag)
def tag_count_increment(sender, instance, created, **kwargs):
	instance.tag.posttagextended.count += 1
	instance.tag.posttagextended.save()

@receiver(post_delete, sender = PostTag)
def tag_count_decrement(sender, instance, **kwargs):
	if instance.tag.posttagextended.count > 0:
		instance.tag.posttagextended.count -= 1
		instance.tag.posttagextended.save()

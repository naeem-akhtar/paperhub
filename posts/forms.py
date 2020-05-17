from django.core.exceptions import ValidationError
from django.conf import settings
from django import forms
from taggit.forms import TagField, TagWidget
from .models import Post


class PostForm(forms.ModelForm):	
	class Meta:
		model = Post
		fields = ['title', 'description', 'document', 'tags']
	
	def clean_tags(self):
		tgs = self.cleaned_data.get('tags', [])
		if len(tgs) > settings.MAX_TAGS_ALLOWED:
			raise ValidationError('Max tags allowed are %s' % settings.MAX_TAGS_ALLOWED, code='invalid')
		else:
			return [t.strip().lower() for t in tgs]
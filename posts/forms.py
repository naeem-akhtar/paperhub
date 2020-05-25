from django.core.exceptions import ValidationError
from django.conf import settings
from django import forms
from taggit.forms import TagField, TagWidget
from ckeditor.widgets import CKEditorWidget
from .models import Post


class PostForm(forms.ModelForm):
	description = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = Post
		fields = ['title', 'description', 'tags', 'document']
	
	def clean_tags(self):
		tgs = self.cleaned_data.get('tags', [])
		if len(tgs) > settings.MAX_TAGS_ALLOWED:
			raise ValidationError('Max tags allowed are %s' % settings.MAX_TAGS_ALLOWED, code='invalid')
		else:
			return [t.strip().lower() for t in tgs]
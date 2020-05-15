import django_filters
from django.db import models
from django.forms.widgets import TextInput
from .models import Post
from hitcount.models import HitCountMixin

class PostFilter(django_filters.FilterSet):
	date_posted = django_filters.DateRangeFilter(
		label = 'date',
		empty_label = 'Date'
	)
	options = django_filters.OrderingFilter(
		label = 'options',
		choices = (
			('latest', 'latest'),
			# ('views', 'most viewed'),
			('bookmark', 'most bookmarked')
		),
		fields = {
			'-date_posted' : 'latest',
			# '-hit_count_generic__hits' : 'views',
			'bookmark' : 'bookmark'
		},
		field_labels={
			'date_posted': 'latest',
			# 'hit_count_generic__hits' : 'views',
			'bookmark' : 'bookmark',
		},
		empty_label = 'Options'
	)
	# author__username = django_filters.CharFilter(
	# 	label='', 
	# 	lookup_expr = 'icontains',
	#   widget=TextInput(attrs={'placeholder': '@username'}),
	#  )
	title = django_filters.CharFilter(
		label = '',
		lookup_expr = 'icontains',
		widget = TextInput(attrs={'placeholder': 'post search'}),
	)

	class Meta:
		model = Post
		fields = ['date_posted']

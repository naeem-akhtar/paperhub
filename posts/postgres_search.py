from itertools import chain
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector
# from posts.models import Post


def post_search_FTB(queryset, text_input):
	search_vector = SearchVector('title', weight='B') + SearchVector('description', weight='C')
	search_queries = SearchQuery(text_input)
	# also add SearchVectorField and index with post model to make it efficient
	# print('serch for :', text_input)
	return queryset \
		.annotate(search = search_vector) \
		.filter(search = search_queries).distinct()

def post_search_tags(queryset, text_input):
	if text_input:
		tags = text_input.split(' ')
		queryset = queryset.filter(tags__name__in = tags).distinct()
	return queryset


def post_search_result(queryset, field_names, text_input):
	return post_search_FTB(queryset, text_input)
	# queryset1 = post_search_FTB(queryset, text_input)
	# queryset2 = post_search_tags(queryset, text_input)
	# return queryset2 | queryset1
	# queryset_final = sorted(
	# 	chain(queryset1, queryset2),
	# 	key=lambda instance: instance.date_posted
	#  )
	# queryset_final = queryset1.union(queryset2)
	# queryset_final = 	queryset1 | queryset2
	# return queryset_final
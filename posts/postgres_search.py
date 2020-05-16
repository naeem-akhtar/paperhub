from django.contrib.postgres.search import SearchQuery, SearchVector
# from posts.models import Post


def post_search_result(queryset, field_names, text_input):
	# add one more vector field for hash tags with weight A
	search_vector = SearchVector('title', weight='B') + SearchVector('description', weight='C')
	search_queries = SearchQuery(text_input)
	# also add SearchVectorField and index with post model to make it efficient

	return queryset \
		.annotate(search = search_vector) \
		.filter(search = search_queries)
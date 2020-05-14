from django.urls import path, include
from .views import (
	PostList, PostDetail, UserPostList, PostCreate, PostUpdate, PostDelete, PostBookmark, UserBookmarkPostList
)

urlpatterns = [
	path('', PostList.as_view(extra_context={'home_page' : 'active'}), name='home'),
	path('ajax/bookmark/', PostBookmark.as_view(), name='bookmark'), # toggle bookmark
	path('posts/bookmark/<str:username>/', UserBookmarkPostList.as_view(extra_context={'bookmark_page' : 'active'}), name='user-bookmarked-posts'),
	path('posts/<str:username>/', UserPostList.as_view(), name='user-posts'), # all post by user
	path('post/new/', PostCreate.as_view(extra_context={'new_post_page' : 'active'}), name='post-create'), # create new post
	path('post/<int:pk>/', PostDetail.as_view(), name='post-detail'),	# a single post
  path('post/<int:pk>/update/', PostUpdate.as_view(), name='post-update'), # update this post
  path('post/<int:pk>/delete/', PostDelete.as_view(), name='post-delete'), # delete this post
  # hit counter for counting views
  path('hitcount/', include('hitcount.urls', namespace='hitcount')),
]

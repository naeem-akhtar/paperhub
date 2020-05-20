from django.urls import path, include
from .views import (
	post_comment, comments_list, delete_comment
)

urlpatterns = [
	path('comments/<int:post_id>', comments_list, name='comments'),
	path('comment/delete/<int:comment_id>', delete_comment, name='comment-delete'),
	# comment on post
	path('post-comment/<int:post_id>/', post_comment, name='post_comment'),
	# comment reply
	path('post-comment/<int:post_id>/<int:parent_comment_id>/', post_comment, name='comment_reply'),
]
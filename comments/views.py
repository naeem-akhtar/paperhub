from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.generic import (
	UpdateView,
	DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
from .models import Comment
from posts.models import Post

# Create your views here.
@login_required
# New parameter parent_comment_id
def post_comment(request, post_id, parent_comment_id=None):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
      comment_form = CommentForm(request.POST)
      if comment_form.is_valid():
        new_comment = comment_form.save(commit=False)
        new_comment.post = post
        new_comment.user = request.user

        # Secondary response
        if parent_comment_id:
          parent_comment = Comment.objects.get(id=parent_comment_id)
          # If the response level exceeds level 2, it will be converted to level 2.
          new_comment.parent_id = parent_comment.get_root().id
          # Respondent
          new_comment.reply_to = parent_comment.user
          new_comment.save()
          return HttpResponse('200 OK')
          # return render(request, 'comments/comment_reply.html', context)
        else:
          new_comment.save()
          return HttpResponse('200 OK')
          # return render(request, 'comments/post_comment.html', context)
      else:
        return HttpResponse ("Invalid comment.")
    elif request.method == 'GET':
      comment_form = CommentForm()
      context = {
        'comment_form': comment_form,
        'post_id': post_id,
        'parent_comment_id': parent_comment_id,
      }
      return render(request, 'comments/comment_form.html', context)
    else:
      return HttpResponse ("Only GET/POST requests are accepted. ")


def comments_list(request, post_id):
  if request.method == 'GET':
    context = {
      'post_id' : post_id,
      'comments' : Comment.objects.filter(post__id = post_id),
    }
    # print(context['comments'])
  return render(request, 'comments/comment_list.html', context)


@login_required
def delete_comment(request, comment_id):
  if request.method == 'POST':
    try:
      comment = Comment.objects.get(pk = comment_id)
      if not comment:
        return HttpResponse('Not a valid comment')
      elif request.user != comment.user:
        return HttpResponse('You are not authorized to perform this action.')
      else:
        comment.delete()
        return HttpResponse('200 OK')
    except Exception as error:
      raise error
  else:
    return HttpResponse('Not a valid request.')


# @login_required
# def update_comment(request, comment_id):
#   if request.method == 'POST':
#     try:
#       comment = Comment.objects.get(pk = comment_id)
#       if not comment:
#         return HttpResponse('Not a valid comment')
#       elif request.user != comment.user:
#         return HttpResponse('You are not authorized to perform this action.')
#       else:
#         comment_form = CommentForm(request.POST)
#         comment.comment = comment_form.cleaned_data['comment']
#         comment.save()
#         return HttpResponse('200 OK')
#     except Exception as error:
#       raise error
#   else:
#     return HttpResponse('Not a valid request.')
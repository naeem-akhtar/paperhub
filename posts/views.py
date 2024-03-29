from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)
from taggit.models import Tag
from .models import Post, Bookmark
from .forms import PostForm
from .filters import PostFilter

User = get_user_model()

# List of multiple posts
class PostList(ListView):
	model = Post
	template_name = 'posts/home.html'
	context_object_name = 'posts'
	paginate_by = 10

	def get_queryset(self):
		queryset = Post.objects.all().order_by('-date_posted')
		self.fpost =  PostFilter(self.request.GET, queryset)
		return self.fpost.qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = self.fpost
		return context


# A single post in detail
class PostDetail(DetailView):
	model = Post
	context_object_name = 'post'

# Posts by a single user
class UserPostList(PostList):
	template_name = 'posts/user_posts.html' # <app>/<model>_<viewtype>.html

	def get_queryset(self):
		queryset = Post.objects.filter(
			author__username = self.kwargs.get('username', None)
		).order_by('-date_posted')
		self.fpost =  PostFilter(self.request.GET, queryset)
		return self.fpost.qs

# Create a post
class PostCreate(LoginRequiredMixin, CreateView):
	model = Post
	form_class = PostForm

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.date_modifed = timezone.now()
		# print(form.cleaned_data)
		return super().form_valid(form)

	def get_success_url(self):
		# print(self.object)
		messages.success(self.request, f'Post created for {self.object.author}')
		return reverse('post-detail', kwargs={'pk' : self.object.pk})


# Update a post
class PostUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Post
	form_class = PostForm

	def form_valid(self, form):
		form.instance.author = self.request.user
		form.instance.date_modifed = timezone.now()
		# print(form.cleaned_data)
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		return (self.request.user == post.author)

	def get_success_url(self):
		# print(self.object)
		messages.success(self.request, f'Post updated by {self.object.author}')
		return reverse('post-detail', kwargs={'pk' : self.object.pk})


# Delete a Post
class PostDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Post
	success_url = '/'

	def test_func(self):
		post = self.get_object()
		return (self.request.user == post.author)


class PostBookmark(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		post_id = request.GET.get('pk', None)
		post = Post.objects.filter(pk = post_id)[0]
		# Bookmark post or get bookmark if already bookmarked
		bookmark_obj, created = Bookmark.objects.get_or_create(user=request.user, post=post)
		# already bookmarked, then unmarked it
		data = {'pk' : post_id}
		if created:
			bookmark_obj.save()
			data['bookmarked'] = 'true'
		else:
			bookmark_obj.delete()
			data['bookmarked'] = 'false'
		return JsonResponse(data)


# Bookmarked posts
class UserBookmarkPostList(LoginRequiredMixin, UserPassesTestMixin, PostList):
	template_name = 'posts/user_bookmark.html' 

	def test_func(self):
		# only the login user can see thier own bookmarks, private stuffs
		return (self.request.user.username == self.kwargs.get('username', None))

	def get_queryset(self):
		queryset = Post.objects.filter(
			bookmark__user__username = self.kwargs.get('username', None)
		).order_by('-date_posted')
		self.fpost =  PostFilter(self.request.GET, queryset)
		return self.fpost.qs


# tag follow unfollow
def tag_follow_toggle(request, pk):
	if request.method == 'GET':
		# print(request.GET)
		operation = request.GET.get('operation', None)	# follow, unfollow, check
		data = {'id' : pk}

		try:
			tag = Tag.objects.get(pk = pk)
			user_id = request.user.pk
			is_following = tag.posttagextended.followers.filter(pk = user_id).exists()

			if operation == 'check':	
				data['status'] = 'followed' if is_following else 'unfollowed'
			elif operation == 'toggle':
				if is_following:
					tag.posttagextended.followers.remove(user_id)
					data['status'] = 'unfollowed'
				else:
					tag.posttagextended.followers.add(user_id)
					data['status'] = 'followed'
			else:
				data['status'] = 'Invalid operation'
		except Exception as error:
			print('Error in tag follow toggle :', error)
			data['status'] = 'Not allowed'

		return JsonResponse(data)
	else:
		return JsonResponse('Not a valid request')


class TagPostList(ListView):
	model = Post
	template_name = 'posts/hashtag.html'
	context_object_name = 'posts'
	paginate_by = 10

	def get_queryset(self):
		self.tag_slug = self.kwargs.get('tag_slug', None)
		queryset = Post.objects.filter(tags__slug__in = [self.tag_slug]).order_by('-date_posted')
		self.fpost =  PostFilter(self.request.GET, queryset)
		return self.fpost.qs

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['filter'] = self.fpost
		context['tag'] = Tag.objects.get(slug = self.tag_slug)
		return context

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.models import Permission
from django.contrib.auth import get_user_model, get_user, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import DetailView, ListView
# Project imports
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, User, UserConnection
from .token import account_activation_token
from posts.models import Post


# register user
def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			try:
				# Make user inactive until they confirm the email
				user = form.save(commit = False)
				# user.is_active = False
				user.save()
				# send email
				current_site = get_current_site(request)
				mail_subject = 'Confirm your email address.'
				message = render_to_string('users/activate_email.html', {
					'user': user,
					'domain': current_site.domain,
					'uid': urlsafe_base64_encode(force_bytes(user.pk)),
					'token': account_activation_token.make_token(user),
	      })
				to_email = form.cleaned_data.get('email')
				email = EmailMessage(
				  mail_subject, message, to=[to_email]
				)
				email.send()
	      # Notify user about confirm email
				username = form.cleaned_data.get('username')
				messages.success(request, f'Account created for {username}. \
					We have send you an email, please confirm it to login.')
				return redirect('login')
			except Exception as error:
				print(error)
				messages.warning(request, f'Cannot SignUp. Try again later.')
	else:
		form = UserRegistrationForm()
	return render(request, 'users/register.html', {'form':form})


# check if username is available
def validate_username(request):
	if request.method == 'GET':
		username = request.GET.get('username', None)
		# print(username)
		data = {
			'is_taken' : User.objects.filter(username__iexact = username).exists()
		}
		if data['is_taken']:
			data['error_message'] = 'A user with this username already exists.'
		return JsonResponse(data)


# User confirm email address
def confirm_email(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user and account_activation_token.check_token(user, token):
		permission = Permission.objects.get(codename='verified')
		user.user_permissions.add(permission)
		user.save()
		# login using ModelBackend to avoid clashases with social account with same email.
		login(request, user, backend='django.contrib.auth.backends.ModelBackend')
		# return redirect('home')
		return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
	else:
		return HttpResponse('Activation link is invalid!')


# Whenever user try to update profile he/she must be loged in
@login_required
def profile_update(request):
	if request.method == 'POST':
		u_form = UserUpdateForm(
			request.POST, 
			instance=request.user
		)
		p_form = ProfileUpdateForm(
			request.POST, 
			request.FILES, 
			instance=request.user.profile
		)
		if u_form.is_valid and p_form.is_valid:
			u_form.save()
			p_form.save()
			messages.success(request, f'Account updated for {request.user.username}!')
			return redirect('profile', username=request.user)
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		
	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request, 'users/profile_form.html', context)
	

# user profile full view
class UserProfile(DetailView):
	model = Profile
	context_object_name = 'profile'

	def get_object(self):
		# print(self.kwargs.get('username'))
		return get_object_or_404(Profile, user__username = self.kwargs.get('username'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		username = self.kwargs.get('username', None)
		context['post_count'] = Post.objects.filter(author__username = username).count()
		context['followers_count'] = UserConnection.objects.filter(following__username = username).count()
		context['following_count'] = UserConnection.objects.filter(follower__username = username).count()
		return context


# To follow / unfollow a user
@login_required
def FollowUser(request):
	if request.method == 'GET':
		operation = request.GET.get('operation', None)
		follower = request.user
		following = User.objects.filter(username = request.GET.get('username', None))[0]
		data = {'username' : following.username}

		if operation == 'change':
			connection, created = UserConnection.objects.get_or_create(
				follower=follower, following = following
			)
			if created:
				connection.save()
				data['status'] = 'followed'
			else:
				connection.delete()
				data['status'] = 'unfollowed'
		elif operation == 'check':
			is_followed = UserConnection.objects.filter(
				follower=follower, following = following).exists()
			if is_followed:
				data['status'] = 'followed'
			else:
				data['status'] = 'unfollowed'

		return JsonResponse(data)


class UserFollower(LoginRequiredMixin, ListView):
	models = User
	template_name = 'users/user_list.html'
	context_object_name = 'users'
	paginate_by = 10

	def get_queryset(self):
		return User.objects.filter(follower__following__username = self.kwargs.get('username', None))


class UserFollowing(LoginRequiredMixin, ListView):
	models = User
	template_name = 'users/user_list.html'
	context_object_name = 'users'
	paginate_by = 10

	def get_queryset(self):
		return User.objects.filter(following__follower__username = self.kwargs.get('username', None))
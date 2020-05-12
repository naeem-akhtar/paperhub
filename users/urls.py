from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from .views import (
  UserProfile, profile_update, register, validate_username, confirm_email,
  FollowUser, UserFollower, UserFollowing
)

urlpatterns = [
  path(r'ajax/validate_username/', validate_username, name='validate_username'),
  path(r'ajax/follow/user/', FollowUser, name='follow_unfollow'),
  path('user/follower/<str:username>/', UserFollower.as_view(), name='followers'),
  path('user/following/<str:username>/', UserFollowing.as_view(), name='following'),
  path('profile/update/', profile_update, name='profile-update'),
  path('profile/<str:username>/', UserProfile.as_view(extra_context={'profile_page' : 'active'}), name='profile'),
  path('register/', register, name='register'),
  re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', confirm_email, name='activate'),
	# build in views for authentication
	path('login/', auth_views.LoginView.as_view(template_name='users/login.html', redirect_authenticated_user=True), name='login'),
  path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
  path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
  path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'), 
  path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
  path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), name='password_reset_complete'),
  # google login using Oauth2
  path('', include('social_django.urls', namespace='social')),
]
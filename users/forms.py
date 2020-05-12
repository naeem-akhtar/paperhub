from django import forms
from .models import User, Profile, UserConnection
from django.contrib.auth.forms import UserCreationForm

# forms
class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=200, help_text='Required')

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

	# email should be unique
	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data.get('email', None)).exists():
			raise forms.ValidationError("This email is already registered.")
		return self.cleaned_data.get('email', None)
		

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']


class DateInput(forms.DateInput):
	input_type = 'date'


class ProfileUpdateForm(forms.ModelForm):
	dob = forms.DateField(widget = DateInput)
	class Meta:
		model = Profile
		fields = ['gender', 'dob', 'image', 'bio']

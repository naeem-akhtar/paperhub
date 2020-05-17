from django import forms
from django.utils import timezone
from .models import User, Profile, UserConnection
from django.contrib.auth.forms import UserCreationForm
import datetime

# helping functions
def no_future_date(value):
	if value >= datetime.date.today():
		raise forms.ValidationError('Invalid Date of Birth')
	return value


# forms
class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=200, help_text='Required')

	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

	# email should be unique
	def clean_email(self):
		email = self.cleaned_data.get('email', None)
		if User.objects.filter(email=email).exists():
			raise forms.ValidationError("This email is already registered.")
		return email
		

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']


class DateInput(forms.DateInput):
	input_type = 'date'


class ProfileUpdateForm(forms.ModelForm):
	dob = forms.DateField(
		widget = forms.SelectDateWidget(
			empty_label=("Year", "Month", "Day"),
			years = range(1900, datetime.datetime.now().year)
		),
		validators=[no_future_date],
	)
	class Meta:
		model = Profile
		fields = ['gender', 'dob', 'image', 'bio']


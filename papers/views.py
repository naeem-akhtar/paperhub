from django.shortcuts import render

# Create your views here.
def about(request):
	context = {
		'about_page' : 'active',
		'title' : 'About'
	}
	return render(request, 'papers/about.html', context)
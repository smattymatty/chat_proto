from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def home(request):
    template = 'welcome_home.html'
    context = {}
    return render(request, template, context)
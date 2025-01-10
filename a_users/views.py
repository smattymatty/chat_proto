from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.
def profile_view(request, username=None):
    try:
        if username:
            profile = get_object_or_404(User, username=username).profile
        else:
            try:
                profile = request.user.profile
            except:
                return redirect_to_login(request.get_full_path())
        return render(request, 'a_users/profile.html', {'profile': profile})
    except User.profile.RelatedObjectDoesNotExist:
        new_profile = Profile()
        new_profile.user = request.user
        new_profile.save()
        return redirect('users:profile', username=request.user.username)
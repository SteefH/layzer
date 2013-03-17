"""Layzer views
"""

from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.template import RequestContext

@login_required
def home(request):
    """The home page view
    """
    from django.template.loaders.app_directories import app_template_dirs
    print app_template_dirs
    return render_to_response(
        'site/index.html',
        context_instance=RequestContext(request)
    )

def login(request):
    """Sign in
    """
    if request.user.is_authenticated():
        return redirect('home')
    return render_to_response(
        'site/accounts/login.html',
        context_instance=RequestContext(request)
    )


@login_required
def logout(request):
    """Sign out
    """
    auth.logout(request)
    return redirect('home')


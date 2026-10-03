from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from .models import UserProfile


def recruiter_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )
        except UserProfile.DoesNotExist:
            messages.error(
                request,
                'User profile not found.'
            )
            return redirect('home')

        if profile.role == 'recruiter':
            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            'Access denied. Recruiter access required.'
        )

        return redirect('candidate_dashboard')

    return wrapper


def candidate_required(view_func):

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        try:
            profile = UserProfile.objects.get(
                user=request.user
            )
        except UserProfile.DoesNotExist:
            messages.error(
                request,
                'User profile not found.'
            )
            return redirect('home')

        if profile.role == 'candidate':
            return view_func(request, *args, **kwargs)

        messages.error(
            request,
            'Access denied. Candidate access required.'
        )

        return redirect('recruiter_dashboard')

    return wrapper
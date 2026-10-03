from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCandidate
from .serializers import CandidateProfileSerializer
from .models import CandidateProfile

from django.shortcuts import render
from .forms import RegisterForm, CandidateProfileForm
from .models import UserProfile, CandidateProfile
from .decorators import recruiter_required, candidate_required

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from .models import UserProfile


def register_view(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data['role']
            )

            login(request, user)

            if form.cleaned_data['role'] == 'recruiter':
                return redirect('recruiter_dashboard')

            return redirect('candidate_dashboard')

    else:
        form = RegisterForm()

    return render(
        request,
        'register.html',
        {'form': form}
    )


def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={'role': 'candidate'}
            )

            if profile.role == 'recruiter':
                return redirect('recruiter_dashboard')

            return redirect('candidate_dashboard')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(request, 'login.html')


def logout_view(request):

    logout(request)

    messages.success(
        request,
        'You have been logged out.'
    )

    return redirect('home')


@login_required
@candidate_required
def candidate_dashboard(request):

    return render(
        request,
        'candidate/dashboard.html'
    )


@login_required
@recruiter_required
def recruiter_dashboard(request):
    from jobs.models import Job
    from applications.models import Application

    jobs = Job.objects.filter(
        recruiter=request.user
    )

    applications = Application.objects.filter(
        job__recruiter=request.user
    )

    context = {
        'total_jobs': jobs.count(),

        'active_jobs': jobs.filter(
            is_active=True
        ).count(),

        'inactive_jobs': jobs.filter(
            is_active=False
        ).count(),

        'total_applications': applications.count(),

        'pending_applications': applications.filter(
            status='pending'
        ).count(),

        'shortlisted_applications': applications.filter(
            status='shortlisted'
        ).count(),

        'interview_applications': applications.filter(
            status='interview'
        ).count(),

        'selected_applications': applications.filter(
            status='selected'
        ).count(),

        'rejected_applications': applications.filter(
            status='rejected'
        ).count(),
    }

    return render(
        request,
        'recruiter/dashboard.html',
        context
    )
@login_required
@candidate_required
def candidate_profile(request):

    profile, created = CandidateProfile.objects.get_or_create(
        user=request.user,
        defaults={
            'full_name': request.user.get_full_name()
            or request.user.username
        }
    )

    if request.method == 'POST':
        form = CandidateProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            candidate_profile = form.save(commit=False)
            candidate_profile.user = request.user
            candidate_profile.save()

            messages.success(
                request,
                'Profile updated successfully!'
            )

            return redirect('candidate_profile')

    else:
        form = CandidateProfileForm(instance=profile)

    return render(
        request,
        'candidate/profile.html',
        {'form': form}
    )

class CandidateProfileAPI(generics.RetrieveUpdateAPIView):
    serializer_class = CandidateProfileSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsCandidate]

    def get_object(self):
        profile, created = CandidateProfile.objects.get_or_create(
            user=self.request.user
        )
        return profile
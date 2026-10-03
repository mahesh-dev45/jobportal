from rest_framework import generics
from rest_framework.permissions import AllowAny
from useraccounts.permissions import IsRecruiter

from django.db.models import Q

from .serializers import JobSerializer

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from useraccounts.decorators import recruiter_required

from .models import Job
from .forms import JobForm


@login_required
@recruiter_required
def create_job(request):

    if request.method == 'POST':

        form = JobForm(request.POST)

        if form.is_valid():

            job = form.save(commit=False)

            job.recruiter = request.user

            job.save()

            messages.success(
                request,
                'Job posted successfully!'
            )

            return redirect('my_jobs')

    else:

        form = JobForm()

    return render(
        request,
        'jobs/create_job.html',
        {'form': form}
    )


@login_required
@recruiter_required
def my_jobs(request):

    jobs = Job.objects.filter(
        recruiter=request.user
    ).order_by('-created_at')

    return render(
        request,
        'jobs/my_jobs.html',
        {'jobs': jobs}
    )


@login_required
@recruiter_required
def edit_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )

    if request.method == 'POST':

        form = JobForm(
            request.POST,
            instance=job
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Job updated successfully!'
            )

            return redirect('my_jobs')

    else:

        form = JobForm(instance=job)

    return render(
        request,
        'jobs/edit_job.html',
        {'form': form}
    )


@login_required
@recruiter_required
def delete_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )

    if request.method == 'POST':

        job.delete()

        messages.success(
            request,
            'Job deleted successfully!'
        )

        return redirect('my_jobs')

    return render(
        request,
        'jobs/delete_job.html',
        {'job': job}
    )




def job_list(request):

    jobs = Job.objects.filter(
        is_active=True
    ).order_by('-created_at')

    search = request.GET.get('search', '').strip()
    location = request.GET.get('location', '').strip()
    job_type = request.GET.get('job_type', '').strip()

    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(skills__icontains=search) |
            Q(description__icontains=search)
        )

    if location:
        jobs = jobs.filter(
            location__icontains=location
        )

    if job_type:
        jobs = jobs.filter(
            job_type=job_type
        )

    context = {
        'jobs': jobs,
        'search': search,
        'location': location,
        'job_type': job_type,
    }

    return render(
        request,
        'jobs/job_list.html',
        context
    )


def job_detail(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    return render(
        request,
        'jobs/job_detail.html',
        {'job': job}
    )

class JobListAPI(generics.ListCreateAPIView):
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsRecruiter()]
        return [AllowAny()]

    def get_queryset(self):
        return Job.objects.filter(
            is_active=True
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(recruiter=self.request.user)


class JobDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsRecruiter()]
        return [AllowAny()]

    def get_queryset(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return Job.objects.filter(
                recruiter=self.request.user
            )

        return Job.objects.all()
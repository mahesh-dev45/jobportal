from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from useraccounts.permissions import IsRecruiter
from useraccounts.permissions import IsCandidate, IsRecruiter


from .serializers import ApplicationSerializer, ApplicationStatusSerializer
from .models import Application

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from useraccounts.decorators import recruiter_required, candidate_required
from django.shortcuts import render, get_object_or_404
from useraccounts.models import CandidateProfile

from jobs.models import Job

from .models import Application, Notification
from .forms import ApplicationForm
from django.utils import timezone


@login_required
@candidate_required
def apply_job(request, job_id):

    job = get_object_or_404(
        Job,
        id=job_id,
        is_active=True
    )

    # Check if application deadline has passed
    if job.deadline < timezone.localdate():

        messages.warning(
            request,
            'The application deadline for this job has passed.'
        )

        return redirect(
            'job_detail',
            job_id=job.id
        )

    # Check if candidate already applied
    existing_application = Application.objects.filter(
        job=job,
        candidate=request.user
    ).first()

    if existing_application:

        messages.warning(
            request,
            'You have already applied for this job.'
        )

        return redirect(
            'job_detail',
            job_id=job.id
        )

    if request.method == 'POST':

        form = ApplicationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            application = form.save(
                commit=False
            )

            application.job = job
            application.candidate = request.user

            application.save()

            messages.success(
                request,
                'Application submitted successfully!'
            )

            return redirect(
                'my_applications'
            )

    else:

        form = ApplicationForm()

    return render(
        request,
        'applications/apply.html',
        {
            'form': form,
            'job': job
        }
    )


@login_required
@candidate_required
def my_applications(request):

    applications = Application.objects.filter(
        candidate=request.user
    ).select_related(
        'job'
    ).order_by(
        '-applied_at'
    )

    return render(
        request,
        'applications/my_applications.html',
        {
            'applications': applications
        }
    )

@login_required
@recruiter_required
def job_applications(request, job_id): 

    job = get_object_or_404(
        Job,
        id=job_id,
        recruiter=request.user
    )

    applications = Application.objects.filter(
        job=job
    ).select_related(
        'candidate'
    ).order_by(
        '-applied_at'
    )

    return render(
        request,
        'applications/job_applications.html',
        {
            'job': job,
            'applications': applications
        }
    )


@login_required
@recruiter_required
def update_application_status(request, application_id):

    application = get_object_or_404(
        Application,
        id=application_id,
        job__recruiter=request.user
    )

    if request.method == 'POST':

        status = request.POST.get('status')

        valid_statuses = [
            'pending',
            'shortlisted',
            'interview',
            'selected',
            'rejected',
        ]

        if status in valid_statuses:

            old_status = application.status

            application.status = status
            application.save()

            if old_status != status:

                Notification.objects.create(
                    user=application.candidate,
                    message=(
                        f"Your application for "
                        f"'{application.job.title}' "
                        f"has been updated to "
                        f"'{application.get_status_display()}'."
                    )
                )

            messages.success(
            request,
            'Application status updated successfully!'
        )

    return redirect(
        'job_applications',
        job_id=application.job.id
    )

@login_required
@candidate_required
def notifications(request):

    notification_list = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'applications/notifications.html',
        {
            'notifications': notification_list
        }
    )

@login_required
@candidate_required
def mark_notification_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    notification.is_read = True
    notification.save(update_fields=['is_read'])

    return redirect('notifications')



class MyApplicationsAPI(generics.ListAPIView):

    serializer_class = ApplicationSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsCandidate]

    def get_queryset(self):
        return Application.objects.filter(
            candidate=self.request.user
        ).order_by('-applied_at')

class JobApplicationsAPI(generics.ListAPIView):

    serializer_class = ApplicationSerializer
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        job_id = self.kwargs['job_id']

        return Application.objects.filter(
            job_id=job_id,
            job__recruiter=self.request.user
        ).order_by('-applied_at')

class ApplicationStatusAPI(generics.UpdateAPIView):
    serializer_class = ApplicationStatusSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsRecruiter]

    def get_queryset(self):
        return Application.objects.filter(
            job__recruiter=self.request.user
        )

    def perform_update(self, serializer):
        application = self.get_object()
        old_status = application.status

        application = serializer.save()

        if old_status != application.status:
            Notification.objects.create(
                user=application.candidate,
                message=(
                    f"Your application for "
                    f"'{application.job.title}' "
                    f"has been updated to "
                    f"'{application.get_status_display()}'."
                )
            )


@login_required
@recruiter_required
def candidate_information(request, application_id):

    application = get_object_or_404(
        Application,
        id=application_id,
        job__recruiter=request.user
    )

    candidate_profile = CandidateProfile.objects.filter(
        user=application.candidate
    ).first()

    context = {
        'application': application,
        'candidate_profile': candidate_profile,
    }

    return render(
        request,
        'applications/candidate_information.html',
        context
    )
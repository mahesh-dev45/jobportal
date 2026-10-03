from django.urls import path
from .views import ApplicationStatusAPI

from .views import (
    apply_job,
    my_applications,
    job_applications,
    update_application_status,
    notifications,
    mark_notification_read,
    MyApplicationsAPI,
    JobApplicationsAPI,
    candidate_information,
)


urlpatterns = [

    path(
        'apply/<int:job_id>/',
        apply_job,
        name='apply_job'
    ),

    path(
        'my-applications/',
        my_applications,
        name='my_applications'
    ),

    path(
        'job/<int:job_id>/',
        job_applications,
        name='job_applications'
    ),

    path(
        'update-status/<int:application_id>/',
        update_application_status,
        name='update_application_status'
    ),

    path(
        'notifications/',
        notifications,
        name='notifications'
    ),

    path(
        'api/my-applications/',
        MyApplicationsAPI.as_view(),
        name='my_applications_api'
    ),

    path(
        'api/job/<int:job_id>/',
        JobApplicationsAPI.as_view(),
        name='job_applications_api'
    ),

    path(
        'api/update-status/<int:pk>/',
        ApplicationStatusAPI.as_view(),
        name='application_status_api'
    ),

    path(
        'candidate/<int:application_id>/',
        candidate_information,
        name='candidate_information'
    ),

    path(
        'notifications/read/<int:notification_id>/',
        mark_notification_read,
        name='mark_notification_read'
    ),
]
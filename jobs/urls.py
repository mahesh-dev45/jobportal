from django.urls import path

from .views import (
    create_job,
    my_jobs,
    edit_job,
    delete_job,
    job_list,
    job_detail,
    JobListAPI,
    JobDetailAPI,
)


urlpatterns = [

    path(
        'create/',
        create_job,
        name='create_job'
    ),

    path(
        'my-jobs/',
        my_jobs,
        name='my_jobs'
    ),

    path(
        'edit/<int:job_id>/',
        edit_job,
        name='edit_job'
    ),

    path(
        'delete/<int:job_id>/',
        delete_job,
        name='delete_job'
    ),

    path(
        '',
        job_list,
        name='job_list'
    ),

    path(
        '<int:job_id>/',
        job_detail,
        name='job_detail'
    ),

    path(
        'api/',
        JobListAPI.as_view(),
        name='job_api_list'
    ),

    path(
        'api/<int:pk>/',
        JobDetailAPI.as_view(),
        name='job_api_detail'
    ),
]
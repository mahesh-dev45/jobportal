from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'recruiter',
        'location',
        'job_type',
        'deadline',
        'is_active',
    )

    list_filter = (
        'job_type',
        'is_active',
        'location',
    )

    search_fields = (
        'title',
        'skills',
        'location',
    )
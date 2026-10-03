from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):

    recruiter_name = serializers.CharField(
        source='recruiter.username',
        read_only=True
    )

    job_type_display = serializers.CharField(
        source='get_job_type_display',
        read_only=True
    )

    class Meta:
        model = Job

        fields = [
            'id',
            'recruiter',
            'recruiter_name',
            'title',
            'description',
            'skills',
            'location',
            'salary',
            'job_type',
            'job_type_display',
            'experience',
            'deadline',
            'created_at',
            'is_active',
        ]

        read_only_fields = [
            'recruiter',
            'created_at',
        ]
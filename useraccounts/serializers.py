
from rest_framework import serializers
from .models import CandidateProfile


class CandidateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CandidateProfile
        fields = [
            'id',
            'full_name',
            'phone',
            'date_of_birth',
            'gender',
            'location',
            'skills',
            'education',
            'experience',
            'resume',
            'profile_photo',
        ]
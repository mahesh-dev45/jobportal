from rest_framework import serializers
from .models import CompanyProfile


class CompanyProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyProfile
        fields = [
            'id',
            'company_name',
            'industry',
            'description',
            'website',
            'email',
            'phone',
            'address',
            'logo',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']
from django.contrib import admin
from .models import CompanyProfile


@admin.register(CompanyProfile)
class CompanyProfileAdmin(admin.ModelAdmin):
    list_display = (
        'company_name',
        'industry',
        'recruiter',
        'email',
        'phone',
    )

    search_fields = (
        'company_name',
        'email',
        'recruiter__username',
    )

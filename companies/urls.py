from django.urls import path
from .views import CompanyProfileAPI

from .views import company_profile


urlpatterns = [
    path(
        'profile/',
        company_profile,
        name='company_profile'
    ),

    path(
        'api/profile/',
        CompanyProfileAPI.as_view(),
        name='company_profile_api'
    ),
]

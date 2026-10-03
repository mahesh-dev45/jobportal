from django.urls import path
from .views import CandidateProfileAPI

from .views import (
    register_view,
    login_view,
    logout_view,
    candidate_dashboard,
    recruiter_dashboard,
    candidate_profile,
)

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path(
        'candidate/dashboard/',
        candidate_dashboard,
        name='candidate_dashboard'
    ),

    path(
        'recruiter/dashboard/',
        recruiter_dashboard,
        name='recruiter_dashboard'
    ),

    path(
        'candidate/profile/',
        candidate_profile,
        name='candidate_profile'    
    ),

    path(
        'api/profile/',
        CandidateProfileAPI.as_view(),
        name='candidate_profile_api'
    ),
]
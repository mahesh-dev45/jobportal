from rest_framework.permissions import BasePermission
from .models import UserProfile


class IsRecruiter(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return UserProfile.objects.filter(
            user=request.user,
            role='recruiter'
        ).exists()


class IsCandidate(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        return UserProfile.objects.filter(
            user=request.user,
            role='candidate'
        ).exists()
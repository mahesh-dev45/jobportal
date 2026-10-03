from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from useraccounts.permissions import IsRecruiter
from .serializers import CompanyProfileSerializer
from .models import CompanyProfile

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from .models import CompanyProfile
from .forms import CompanyProfileForm
from useraccounts.decorators import recruiter_required


@login_required
@recruiter_required
def company_profile(request):

    profile, created = CompanyProfile.objects.get_or_create(
        recruiter=request.user,
        defaults={
            'company_name': '',
            'industry': 'IT',
            'description': '',
            'email': request.user.email,
            'phone': '',
            'address': '',
        }
    )

    if request.method == 'POST':

        form = CompanyProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():

            company = form.save(commit=False)
            company.recruiter = request.user
            company.save()

            messages.success(
                request,
                'Company profile updated successfully!'
            )

            return redirect('company_profile')

    else:
        form = CompanyProfileForm(
            instance=profile
        )

    return render(
        request,
        'recruiter/company_profile.html',
        {'form': form}
    )

class CompanyProfileAPI(generics.RetrieveUpdateAPIView):
    serializer_class = CompanyProfileSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [IsRecruiter]

    def get_object(self):
        profile, created = CompanyProfile.objects.get_or_create(
            recruiter=self.request.user,
            defaults={
                'company_name': '',
                'industry': 'Other',
                'description': '',
                'email': self.request.user.email,
                'phone': '',
                'address': '',
            }
        )
        return profile
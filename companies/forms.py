from django import forms
from .models import CompanyProfile


class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = CompanyProfile

        fields = [
            'company_name',
            'industry',
            'description',
            'website',
            'email',
            'phone',
            'address',
            'logo',
        ]

        widgets = {
            'description': forms.Textarea(
                attrs={'rows': 4}
            ),

            'address': forms.Textarea(
                attrs={'rows': 3}
            ),
        }
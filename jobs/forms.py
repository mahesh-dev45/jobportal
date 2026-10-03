from django import forms
from .models import Job


class JobForm(forms.ModelForm):

    class Meta:
        model = Job

        fields = [
            'title',
            'description',
            'skills',
            'location',
            'salary',
            'job_type',
            'experience',
            'deadline',
            'is_active',
        ]

        widgets = {

            'description': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Enter job description'
                }
            ),

            'skills': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Python, Django, SQL...'
                }
            ),

            'deadline': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
        }
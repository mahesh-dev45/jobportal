from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CandidateProfile

class RegisterForm(UserCreationForm):

    email = forms.EmailField()

    ROLE_CHOICES = [
        ('candidate', 'Candidate'),
        ('recruiter', 'Recruiter'),
    ]

    role = forms.ChoiceField(
        choices=ROLE_CHOICES
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'role'
        ]



class CandidateProfileForm(forms.ModelForm):

    class Meta:
        model = CandidateProfile
        fields = [
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

        widgets = {
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date'}
            ),
            'skills': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Python, Django, SQL, HTML...'
                }
            ),
            'education': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'MCA, BCA, etc.'
                }
            ),
            'experience': forms.Textarea(
                attrs={
                    'rows': 3,
                    'placeholder': 'Fresher / 1 year experience...'
                }
            ),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')

        if resume:
            allowed_extensions = ['.pdf', '.doc', '.docx']

            if not any(
                resume.name.lower().endswith(ext)
                for ext in allowed_extensions
            ):
                raise forms.ValidationError(
                    'Resume must be PDF, DOC, or DOCX format.'
                )

            max_size = 5 * 1024 * 1024

            if resume.size > max_size:
                raise forms.ValidationError(
                    'Resume file size must not exceed 5 MB.'
                )

        return resume

    def clean_profile_photo(self):
        photo = self.cleaned_data.get('profile_photo')

        if photo:
            allowed_extensions = ['.jpg', '.jpeg', '.png']

            if not any(
                photo.name.lower().endswith(ext)
                for ext in allowed_extensions
            ):
                raise forms.ValidationError(
                    'Profile photo must be JPG, JPEG, or PNG format.'
                )

            max_size = 2 * 1024 * 1024

            if photo.size > max_size:
                raise forms.ValidationError(
                    'Profile photo size must not exceed 2 MB.'
                )

        return photo
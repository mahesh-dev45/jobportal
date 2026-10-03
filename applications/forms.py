from django import forms
from .models import Application


from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application

        fields = [
            'resume',
            'cover_letter',
        ]

        widgets = {
            'cover_letter': forms.Textarea(
                attrs={
                    'rows': 6,
                    'placeholder': 'Write your cover letter...'
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
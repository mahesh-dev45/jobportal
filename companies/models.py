from django.db import models
from django.contrib.auth.models import User


class CompanyProfile(models.Model):

    INDUSTRY_CHOICES = [
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Manufacturing', 'Manufacturing'),
        ('Healthcare', 'Healthcare'),
        ('Education', 'Education'),
        ('Other', 'Other'),
    ]

    recruiter = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    company_name = models.CharField(max_length=200)

    industry = models.CharField(
        max_length=50,
        choices=INDUSTRY_CHOICES
    )

    description = models.TextField()

    website = models.URLField(
        blank=True
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    address = models.TextField()

    logo = models.ImageField(
        upload_to='company_logos/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.company_name
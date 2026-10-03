# Job Portal & Recruitment Management System

A full-stack web-based Job Portal and Recruitment Management System developed using Django and Django REST Framework.

## Features

### Candidate
- Candidate registration and login
- Candidate profile management
- Resume and profile photo upload
- Browse available jobs
- Search and filter jobs
- Apply for jobs
- Prevent duplicate applications
- View application history
- Application status notifications

### Recruiter
- Recruiter registration and login
- Company profile management
- Create and manage jobs
- Edit and delete own jobs
- View job applications
- View candidate information
- Download candidate resumes
- Update application status

### Security
- Authentication and role-based authorization
- Candidate/Recruiter access control
- Job ownership validation
- Application ownership validation
- File upload validation
- Resume size/type validation
- Job deadline protection
- Duplicate application protection
- API permissions

### REST API
- Job APIs
- Candidate profile API
- Company profile API
- My applications API
- Job applications API
- Application status API

## Technology Stack

- Python
- Django
- Django REST Framework
- HTML5
- CSS3
- JavaScript
- Bootstrap 5
- SQLite / MySQL
- Pillow
- Git & GitHub

## Project Structure

```text
jobportal/
├── applications/
├── companies/
├── jobs/
├── useraccounts/
├── templates/
├── static/
├── media/
├── manage.py
└── README.md
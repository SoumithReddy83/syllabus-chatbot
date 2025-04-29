from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

# Custom User Model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def __str__(self):
        return self.username
    

class Syllabus(models.Model):
    professor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)
    course_number = models.CharField(max_length=20)
    course_name = models.CharField(max_length=100)
    syllabus_file = models.FileField(upload_to='syllabi/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.course_name} ({self.course_number}) - {self.department}"

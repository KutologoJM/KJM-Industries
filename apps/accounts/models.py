"""
Django ORM model definitions for this app.

Docs: https://docs.djangoproject.com/en/stable/topics/db/models/

Rules:
    - Models are pure data definitions — field declarations, Meta, and __str__ only.
    - Attach custom managers from managers.py for reusable queryset building blocks.
    - No business logic in models — that belongs in services.
    - No query composition in models — that belongs in selectors.
    - Use explicit field names and avoid relying on Django defaults for null/blank.

Example:
    class Post(models.Model):
        title = models.CharField(max_length=200)
        body = models.TextField()
        author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
        status = models.CharField(max_length=20, choices=PostStatus.choices, default=PostStatus.DRAFT)
        created_at = models.DateTimeField(auto_now_add=True)

        objects = models.Manager()
        published = PublishedManager()

        class Meta:
            ordering = ["-created_at"]

        def __str__(self):
            return self.title
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from core.models import TimeStampedModel


# Create your models here.
class CustomUser(AbstractUser):
    pass


class Department(TimeStampedModel):
    """
    Holds key information about the 5 departments in KJM Industries.
    - Agriculture
    - Transportation
    - Manufacturing
    - Sales
    - Storage
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)


class EmployeeProfile(TimeStampedModel):
    """
    User profile for employees working in KJM Industries.
    """
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="employees")
    role = models.CharField(
        max_length=100,
        choices=(
            ("admin", "Admin"),
            ("manager", "Manager"),
            ("employee", "Employee"),
        ),
        default="employee",
    )

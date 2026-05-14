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

# Shared models
from django.db import models
from django_extensions.db.fields import AutoSlugField, ModificationDateTimeField, CreationDateTimeField
import uuid


class TimeStampedModel(models.Model):
    created_at = CreationDateTimeField()
    updated_at = ModificationDateTimeField()

    class Meta:
        abstract = True


class TimeStampedUUIDModel(TimeStampedModel):
    """
    uid is public-facing while id is for internal use.
    """
    uid = models.UUIDField(
        unique=True,
        default=uuid.uuid8,
        editable=False,
        db_index=True,
    )

    class Meta:
        abstract = True


class BaseItem(TimeStampedModel):
    """
    A common base model for all items that each department will have.
    Slug instead of uuid to make it easier to reference items in the API.
    """
    name = models.CharField(max_length=50)
    slug = AutoSlugField(populate_from="name")
    image_url = models.URLField(blank=True, null=True)

    class Meta:
        abstract = True


class BaseFacility(TimeStampedUUIDModel):
    """
    A common base model for all facility types.
    """
    name = models.CharField(max_length=50)
    image_url = models.URLField(blank=True, null=True)

    # location

    class Meta:
        abstract = True

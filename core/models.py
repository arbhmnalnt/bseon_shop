from django.db import models

class BaseModel(models.Model):
    """A reusable base model with soft delete functionality."""

    created_at = models.DateTimeField(auto_now_add=True)  # Set when created
    updated_at = models.DateTimeField(auto_now=True)      # Set on every save
    is_active = models.BooleanField(default=True)         # Soft delete flag

    def delete(self, *args, **kwargs):
        """Override delete method to perform soft delete."""
        self.is_active = False
        self.save()

    class Meta:
        abstract = True  # Prevent Django from creating a separate table for BaseModel

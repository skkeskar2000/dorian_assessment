import uuid

from django.db import models


class BaseModelMixin(models.Model):
    id = models.UUIDField(primary_key=True, null=False, blank=False, default=uuid.uuid4)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    validator = None

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def save_without_validation(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def validate(self, **kwargs):
        self.validator.validate(**kwargs) if self.validator else None

    class Meta:
        abstract = True

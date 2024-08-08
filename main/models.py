from django.db import models

from dorian_assessment.model.base_model import BaseModelMixin
from main.enum import LOBEnum


# Create your models here.
class Category(BaseModelMixin):
    clubbed_name = models.CharField(null=False, blank=False, max_length=100)
    category = models.CharField(null=False, blank=False, max_length=100)


class Name(BaseModelMixin):
    insurance = models.CharField(null=False, blank=False, max_length=100)
    name = models.CharField(null=False, blank=False, max_length=100)
    clubbed_name = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)


class UploadFile(BaseModelMixin):
    file = models.FileField(upload_to='excel/')


class InsuranceData(BaseModelMixin):
    date = models.DateField(null=False, blank=False)
    name = models.ForeignKey(Name, on_delete=models.CASCADE, null=False, blank=False)
    product = models.CharField(choices=LOBEnum.get_choices(), null=False, blank=False, max_length=100)
    value = models.FloatField(null=False, blank=False)

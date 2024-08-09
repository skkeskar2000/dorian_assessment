import re
from datetime import datetime
import numpy as np
import pandas as pd
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError
from dorian_assessment.model.base_model import BaseModelMixin
from main.enum import LOBEnum, FileUploadStatusEnum


class Category(BaseModelMixin):
    clubbed_name = models.CharField(null=False, blank=False, max_length=100)
    category = models.CharField(null=False, blank=False, max_length=100)


class Name(BaseModelMixin):
    insurance = models.CharField(null=False, blank=False, max_length=100)
    name = models.CharField(null=False, blank=False, max_length=100)
    clubbed_name = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)


class UploadFile(BaseModelMixin):
    file = models.FileField(upload_to='media/excel/')
    upload_status = models.CharField(null=False, blank=False, choices=FileUploadStatusEnum.get_choices(),
                                     default=FileUploadStatusEnum.INITIATED.value, max_length=20)

    def extract_date(self, description):
        date_pattern = r'\b(\w+\s+\d{4})\b'

        match = re.search(date_pattern, description)

        if match:
            date_str = match.group(1)
            try:
                date_obj = datetime.strptime(date_str, '%B %Y')
                return date_obj
            except ValueError:
                return date_str
        return None

    def validate(self):
        if not self.extracted_date:
            raise ValidationError('Invalid date')

    def handle_upload(self):

        self.upload_status = FileUploadStatusEnum.PROCESSING.value
        self.save()
        data = None
        try:
            self.parse_excel_file()
            self.validate()
            data = self.process_file()
            self.upload_status = FileUploadStatusEnum.SUCCESS.value
        except Exception as e:
            self.error = str(e)
            self.upload_status = FileUploadStatusEnum.FAILED.value
        self.save()
        return data

    def parse_excel_file(self):
        xls = pd.ExcelFile(self.file.path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            df = df.replace(np.nan, None)

            if df.iloc[0, 0]:
                description = df.iloc[0, 0]
                df = df.drop(0).reset_index(drop=True)
            else:
                description = df.columns[0]

            column_headings = df.iloc[0, 0:].values.tolist()
            first_column_heading = df.iloc[1, 0]
            self.data = df.iloc[2:, :].reset_index(drop=True)
            column_headings.insert(0, first_column_heading)

            self.column_headings = column_headings
            self.extracted_date = self.extract_date(description)

    def process_file(self):
        rows = []
        if self.extracted_date:
            for index, row in self.data.iterrows():
                for i in range(len(self.column_headings)):
                    if row.iloc[0] != "Previous Year":
                        product = LOBEnum.search_by_value(self.column_headings[i])
                        rows.append(row)
                        with transaction.atomic():
                            if product:
                                name = Name.objects.filter(insurance=row.iloc[0])
                                if name.first():
                                    InsuranceData.objects.create(date=self.extracted_date.date(), name=name.first(),
                                                                 product=product.value, value=row.iloc[i])
        return rows


class InsuranceData(BaseModelMixin):
    date = models.DateField(null=False, blank=False)
    name = models.ForeignKey(Name, on_delete=models.CASCADE, null=False, blank=False)
    product = models.CharField(choices=LOBEnum.get_choices(), null=False, blank=False, max_length=100)
    value = models.FloatField(null=False, blank=False)


@receiver(post_save, sender=UploadFile)
def send_notification_on_schedule_create_athletes(sender, instance: UploadFile, created, **kwargs):
    if created:
        instance.handle_upload()

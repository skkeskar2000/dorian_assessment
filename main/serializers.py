import os

import pandas as pd
from rest_framework import serializers

from dorian_assessment import settings
from main.models import UploadFile, InsuranceData


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'

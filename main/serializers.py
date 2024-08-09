from rest_framework import serializers
from main.models import UploadFile, InsuranceData


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'


class InsuranceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceData
        fields = ['id', 'date', 'name', 'product', 'value']

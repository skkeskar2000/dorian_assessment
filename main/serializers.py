from rest_framework import serializers
from main.models import UploadFile, InsuranceData, Name


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'


class NameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Name
        fields = ['id', 'insurance', 'name', 'clubbed_name']


class InsuranceDataSerializer(serializers.ModelSerializer):
    name = NameSerializer()  # Use the nested serializer for 'name'

    class Meta:
        model = InsuranceData
        fields = ['id', 'date', 'name', 'product', 'value']

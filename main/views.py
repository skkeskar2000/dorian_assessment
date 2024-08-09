import pandas as pd
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination

from main.models import Name, InsuranceData
from main.serializers import UploadFileSerializer, InsuranceDataSerializer


class InsuranceDataPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class UploadExcel(CreateAPIView):
    serializer_class = UploadFileSerializer


class InsuranceDataListView(ListAPIView):
    queryset = InsuranceData.objects.all()
    serializer_class = InsuranceDataSerializer
    pagination_class = InsuranceDataPagination


def generate_excel(request):
    insurance_data = InsuranceData.objects.select_related('name__clubbed_name').all()

    data = []
    for item in insurance_data:
        row = {
            'Year': item.date.year,
            'Month': item.date.month,
            'Category': item.name.clubbed_name.clubbed_name,
            'Clubbed_name': item.name.insurance,
            'Product': item.product,
            'Value': item.value
        }
        data.append(row)

    df = pd.DataFrame(data)

    with pd.ExcelWriter('insurance_data.xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='InsuranceData')

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="insurance_data.xlsx"'

    with open('insurance_data.xlsx', 'rb') as f:
        response.write(f.read())

    return response

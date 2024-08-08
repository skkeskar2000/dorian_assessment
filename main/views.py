from datetime import datetime
import numpy as np
import pandas as pd
import re

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from main.enum import LOBEnum
from main.models import Name, InsuranceData
from main.serializers import UploadFileSerializer


# Create your views here.


class UploadExcel(CreateAPIView):
    serializer_class = UploadFileSerializer

    def post(self, request, *args, **kwargs):
        file = request.data['file']
        with open('temp.xlsx', 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            xls = pd.ExcelFile('temp.xlsx')
            sheets_data = {}
            for sheet_name in xls.sheet_names:
                print(sheet_name)
                df = pd.read_excel(xls, sheet_name=sheet_name)
                df = df.replace(np.nan, None)

                if df.iloc[0, 0]:
                    description = df.iloc[0, 0]
                    df = df.drop(0).reset_index(drop=True)
                else:
                    description = df.columns[0]

                column_headings = df.iloc[0, 0:].values.tolist()
                first_column_heading = df.iloc[1, 0]
                data = df.iloc[2:, :].reset_index(drop=True)

                column_headings.insert(0, first_column_heading)
                extracted_date = extract_date(description)
                if extracted_date:
                    for index, row in data.iterrows():
                        for i in range(len(column_headings)):
                            if row[0] is not "Previous Year":
                                product = LOBEnum.search_by_value(column_headings[i])
                                with transaction.atomic():
                                    if product:
                                        name = Name.objects.filter(insurance=row[0])
                                        if name.first():
                                            InsuranceData.objects.create(date=extracted_date.date(), name=name.first(),
                                                                         product=product.value, value=row[i])

                sheets_data[sheet_name] = df.to_dict(orient='records')

            # TODO: Clean up the temporary file
            import os
            os.remove('temp.xlsx')

        return Response({"success": "success"})


def extract_date(description):
    # Define a regex pattern to match "January 2024"
    date_pattern = r'\b(\w+\s+\d{4})\b'

    # Search for the pattern in the description
    match = re.search(date_pattern, description)

    if match:
        # Extract the matched string
        date_str = match.group(1)
        try:
            # Convert the string to a datetime object (Optional)
            date_obj = datetime.strptime(date_str, '%B %Y')
            return date_obj
        except ValueError:
            return date_str  # Return the raw string if parsing fails
    return None


def generate_excel(request):
    # Query the data
    insurance_data = InsuranceData.objects.select_related('name__clubbed_name').all()

    # Transform the data into the required format
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

    # Create a DataFrame
    df = pd.DataFrame(data)

    # Generate an Excel file
    with pd.ExcelWriter('insurance_data.xlsx') as writer:
        df.to_excel(writer, index=False, sheet_name='InsuranceData')

    # Return the Excel file as a response
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="insurance_data.xlsx"'

    # Write the Excel file to the response
    with open('insurance_data.xlsx', 'rb') as f:
        response.write(f.read())

    return response

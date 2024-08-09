from django.urls import path

from main.views import UploadExcel, generate_excel

urlpatterns = [
    path('generate-excel/', generate_excel, name='generate_excel'),
    path('upload-excel/', UploadExcel.as_view(), name='upload_excel')
]

from django.urls import path

from main.views import UploadExcel, generate_excel, InsuranceDataListView

urlpatterns = [
    path('generate-excel/', generate_excel, name='generate_excel'),
    path('upload-excel/', UploadExcel.as_view(), name='upload_excel'),
    path('insurance-data/', InsuranceDataListView.as_view(), name='insurance-data-list'),

]

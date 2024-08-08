from django.contrib import admin

from main.models import Category, Name

# Register your models here.

import pandas as pd
from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from .models import Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('clubbed_name', 'category')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.admin_site.admin_view(self.upload_excel), name='category-upload-excel'),
        ]
        return custom_urls + urls

    def upload_excel(self, request):
        if request.method == 'POST':
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                Category.objects.create(
                    clubbed_name=row['clubbed_name'],
                    category=row['category']
                )
            self.message_user(request, "Data uploaded successfully.")
            return render(request, 'admin/upload_excel.html')

        return render(request, 'admin/upload_excel.html')


admin.site.register(Category, CategoryAdmin)


class NameAdmin(admin.ModelAdmin):
    list_display = ('insurance', 'name', 'clubbed_name')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.admin_site.admin_view(self.upload_excel), name='name-upload-excel'),
        ]
        return custom_urls + urls

    def upload_excel(self, request):
        if request.method == 'POST':
            excel_file = request.FILES['excel_file']
            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                try:
                    category = Category.objects.get(clubbed_name=row['clubbed_name'])
                except Category.DoesNotExist:
                    continue

                Name.objects.create(
                    insurance=row['insurance'],
                    name=row['name'],
                    clubbed_name=category
                )
            self.message_user(request, "Data uploaded successfully.")
            return render(request, 'admin/upload_excel.html')

        return render(request, 'admin/upload_excel.html')


admin.site.register(Name, NameAdmin)

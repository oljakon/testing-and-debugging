from django.contrib import admin
from .models import City, Industry, Company, JobVacancy, Application

admin.site.register(City)
admin.site.register(Industry)
admin.site.register(Company)
admin.site.register(JobVacancy)
admin.site.register(Application)

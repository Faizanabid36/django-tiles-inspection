from django.contrib import admin
from . import models

admin.site.register(models.EmployeeModel)
admin.site.register(models.InspectionModel)

# Register your models here.

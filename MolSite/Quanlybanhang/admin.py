from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Workingstatus)
admin.site.register(models.Paymentstatus)
# admin.site.register(models.Donhang)
admin.site.register(models.Customer)
admin.site.register(models.Source)
admin.site.register(models.Product)
admin.site.register(models.Donhang)



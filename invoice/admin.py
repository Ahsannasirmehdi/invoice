from django.contrib import admin
from .models import *





class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'customer']
    list_filter = ['user']





admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Profile)
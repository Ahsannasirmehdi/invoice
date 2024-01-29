import os
from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from django import forms
SUBSCRIPTION = (
    ('F', 'FREE'),
    ('M', 'MONTHLY'),
    ('Y', 'YEARLY'),
)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_pro = models.BooleanField (default=False)
    pro_expiry_date= models.DateTimeField(null=True, blank=True)
    subscription_type = models.CharField(max_length=100, choices=SUBSCRIPTION, default="FREE")
# Create your models here.

def get_template_files():
    # Path to the directory containing your template files

    template_directory = 'invoice/templates/invoice/custom'

    # Fetch all files in the directory
    files = os.listdir(template_directory)

    # Filter HTML files
    html_files = [file_name for file_name in files if file_name.endswith('.html')]

    # Create choices list with tuples of (file_name, file_name)
    choices = [(file_name, file_name) for file_name in html_files]

    return choices


# class temp(models.Model):
#     # Fetch file names dynamically and set as choices
#     COLOR_CHOICES = get_template_files()
#     template_options = models.CharField(max_length=100, choices=COLOR_CHOICES)
#
#     def __str__(self):
#         return self.template_options
# @admin.register(temp)
# class TempAdmin(admin.ModelAdmin):
#         list_display = ('id', 'template_options')
class Invoice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    customer = models.TextField(default='')
    contact = models.CharField(max_length=255, default='', blank=True, null=True)
    email = models.EmailField(default='', blank=True, null=True)
    comments = models.TextField(default='', blank=True, null=True)
    content = RichTextUploadingField()
    pdf_document = models.FileField(upload_to='invoices_pdf/')

    def __str__(self):
        return str(self.id)













from django import forms
from django.forms import formset_factory
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *





# class CustomerForm(forms.ModelForm):
#     class Meta:
#         model = Customer
#         fields = [
#             'customer_name',
#             'customer_gender',
#             'customer_dob',
#         ]
#         widgets = {
#             'customer_name': forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'id': 'customer_name',
#                 'placeholder': 'Enter name of the customer',
#             }),
#             'customer_gender': forms.Select(attrs={
#                 'class': 'form-control',
#                 'id': 'customer_gender',
#             }),
#             'customer_dob': forms.DateInput(attrs={
#                 'class': 'form-control',
#                 'id': 'customer_dob',
#                 'placeholder': '2000-01-01',
#                 'type': 'date',
#             }),
#         }


class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = [
            'customer',
            'comments',
            'contact',
            'email',
            # 'content',
            # 'pdf_document',
        ]
        widgets = {
            'customer': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_customer',
                'placeholder': 'Enter name of the customer',
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_contact',
                'placeholder': 'Enter contact of the customer',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'invoice_email',
                'placeholder': 'Enter email of the customer',
            }),
            'comments': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'invoice_comments',
                'placeholder': 'Enter comments',
            }),



        }






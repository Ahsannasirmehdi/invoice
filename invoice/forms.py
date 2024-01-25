from django import forms
from django.forms import formset_factory
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import *


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'address',
            'general',
            'company',
            'date',
            'demand',
            'general',
        ]
        widgets = {
            'product_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'product_name',
                'placeholder': 'Enter name of the product',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'add',
                'placeholder': 'Enter name of the address',
            }),
            'general': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'general',
                'placeholder': 'Enter name of the general',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'company',
                'placeholder': 'Enter name of the company',
            }),
            'date': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'date',
               'placeholder': 'Enter name of the date',
            }),
            'demand': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'demand',
                'placeholder': 'Enter name of the demand',
            }),



        }


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

class InvoiceDetailForm(forms.ModelForm):
    amount = forms.Select(choices=InvoiceDetail.COLOR_CHOICES)
    class Meta:
        model = InvoiceDetail
        fields = [
            'product',
            'amount',
        ]
        widgets = {
            'product': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_product',
            }),
            'amount': forms.Select(attrs={
                'class': 'form-control',
                'id': 'invoice_detail_template_options',

            })
        }


class excelUploadForm(forms.Form):
    file = forms.FileField()


InvoiceDetailFormSet = formset_factory(InvoiceDetailForm, extra=1)

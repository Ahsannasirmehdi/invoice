from datetime import datetime, timedelta
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.models import Session
from django.views.decorators.cache import never_cache
from utils.filehandler import handle_file_upload
from django.shortcuts import render, redirect
from django.utils import timezone
# from datetime import
from django.conf import settings
from celery import shared_task
from django.core.mail import EmailMessage
from django.forms import modelformset_factory
from weasyprint import HTML
import stripe
from .forms import *
from .models import *
import pandas as pd
from django_weasyprint.views import WeasyTemplateResponse
# Create your views here.
from django.core.files.base import ContentFile
import smtplib
from email.message import EmailMessage

from docx import Document

# from ...voicegen.invoices.models import OrderLine


def schedule(request):
    return render(request, "invoice/schedule.html")


def base(request):
    # total_customer = Customer.objects.count()
    product = InvoiceForm()
    context = {
        # "total_customer": total_customer,
        "total_invoice": product,

    }
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        try:
         request.session['profile'] = profile.is_pro
         print('new')
        except:
            print()

    return render(request, "invoice/base/base.html", context)


# Function to send reminders

def home(requests):
    return  render(requests,'invoice/index.html')

# Modify your existing sub function to call the generate_invoices task



def delete_all_invoice(request):
    # Delete all invoice
    if request.method == "POST":
        Invoice.objects.all().delete()
        return redirect('view_invoice')

    return render(request, "invoice/del.html")


def adin(request):
    return render(request, "invoice/admin.html")


def addata(request):
    n = Profile.objects.all()
    context = {'profiles': n}
    return render(request, "invoice/admindata.html", context)
def registerusers(request):
    n = User.objects.all()
    context = {'profiles': n}
    return render(request, "invoice/regusers.html", context)





def create_product(request):
    total_product = Product.objects.count()
    # print(total_product)
    # total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    # total_income = getTotalIncome()

    product = ProductForm()

    if request.method == "POST":
        product = ProductForm(request.POST)
        if product.is_valid():
            product.save()
            return redirect("create_product")

    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,
        # "total_income": total_income,
        "product": product,
    }

    return render(request, "invoice/create_product.html", context)


def view_product(request):
    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()

    product = Product.objects.filter(product_is_delete=False)
    print(product)
    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,

        "product": product,
    }

    return render(request, "invoice/view_product.html", context)


def create_invoice(request):

    form = InvoiceForm()

    if request.method == "POST":
        form = InvoiceForm(request.POST)

        if form.is_valid():
            print('ew')
            content = request.POST.get('content')
            email = request.POST.get('email')
            invoice = Invoice.objects.create(
                customer=form.cleaned_data.get("customer"),
                contact=form.cleaned_data.get("contact"),
                email=form.cleaned_data.get("email"),
                date=form.cleaned_data.get("comments"),
            )

            print(email)
            if content:
                print('ml')
                # Get content from POST request
                content = request.POST.get('content')
                # Create a temporary HTML file
                html_filename = 'temp.html'
                with open(html_filename, 'w', encoding='utf-8') as html_file:
                    html_file.write(content)
                invoice_id = invoice.id
                # Convert HTML to PDF using WeasyPrint
                pdf_filename = os.path.join(settings.BASE_DIR, 'invoice', 'templates', 'invoice', 'pdfs', str(invoice_id))
                HTML(string=content).write_pdf(pdf_filename)

                # Read the PDF file
                with open(pdf_filename, 'rb') as pdf_file:
                    response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                    response['Content-Disposition'] = 'inline; filename=output.pdf'
                send_email_with_attachment(pdf_filename, email)
                # Cleanup: Remove temporary HTML and PDF files
                os.remove(html_filename)


            invoice.save()

            return redirect("view_invoice")

        else:
            # Print form errors and file information to the console
            print(f"Form errors in file: {__file__}")
            for field, errors in form.errors.items():
                print(f"Field: {field}, Errors: {', '.join(errors)}")

    context = {

        "form": form,
        # "formset": formset,
        # "saved_content":saved_content,
    }

    return render(request, "invoice/create_invoice.html", context)


def template(request):
    return render(request, 'invoice/custom/new.html')


def view_invoice(request):
    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()

    invoice = Invoice.objects.all()

    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,
        # "total_income": total_income,
        "invoice": invoice,
    }

    return render(request, "invoice/view_invoice.html", context)

from django.views.decorators.cache import cache_control

@never_cache
def logout_view(request):
    # Use the built-in logout function without passing any arguments
    logout(request)
    request.session.flush()
    return redirect('/home')


# Detail view of invoices
def view_invoice_detail(request, pk):
    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    # total_income = getTotalIncome()

    invoice = Invoice.objects.get(id=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)

    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,
        # "total_income": total_income,
        # 'invoice': invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "invoice/view_invoice_detail.html", context)


# Delete invoice
def delete_invoice(request, pk):
    total_product = Product.objects.count()
    # total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    try:
        invoice = Invoice.objects.get(id=pk)
    except Invoice.DoesNotExist:
     # If the invoice with the specified id does not exist, you can redirect to a different URL
        return redirect('view_invoice')
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    if request.method == "POST":
        invoice_detail.delete()
        invoice.delete()
        return redirect("view_invoice")

    context = {
        "total_product": total_product,
        # "total_customer": total_customer,
        "total_invoice": total_invoice,

        "invoice": invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "invoice/delete_invoice.html", context)


def edit_product(request, pk):
    total_product = Product.objects.count()
    total_invoice = Invoice.objects.count()

    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("view_product")
    else:
        form = ProductForm(instance=product)

    context = {
        "total_product": total_product,
        "total_invoice": total_invoice,

        "product": form,
    }

    return render(request, "invoice/create_product.html", context)


def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)
    InvoiceDetailFormSet = modelformset_factory(InvoiceDetail, form=InvoiceDetailForm, extra=1)

    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        formset = InvoiceDetailFormSet(request.POST, queryset=InvoiceDetail.objects.filter(invoice=invoice))

        if form.is_valid() or formset.is_valid():
            form.save()

            for detail_form in formset:
                if detail_form.is_valid():
                    product = detail_form.cleaned_data.get("product")
                    amount = detail_form.cleaned_data.get("amount")

                    # Update or create InvoiceDetail instances
                    InvoiceDetail.objects.update_or_create(
                        invoice=invoice,
                        product=product,
                        defaults={'amount': amount}  # Update amount if exists or create new instance
                    )

            return redirect("view_invoice")

    else:
        form = InvoiceForm(instance=invoice)
        formset = InvoiceDetailFormSet(queryset=InvoiceDetail.objects.filter(invoice=invoice))

    context = {
        "form": form,
        "formset": formset,
        "invoice": invoice,
    }

    return render(request, "invoice/create_invoice.html", context)


GMAIL = 'amaramarylene@gmail.com'  # email
GMAIL_PASSWORD = 'fqwk kork ozcs vaws'  # pass


def send_email_with_attachment(pdf_file_path, recipient_email):
    # Create EmailMessage object
    msg = EmailMessage()
    msg['From'] = GMAIL
    msg['To'] = recipient_email
    msg['Subject'] = 'Invoice PDF'

    # Set the body of the email (optional)
    msg.set_content('Please find the attached invoice PDF.')


    # Open the PDF file
    with open(pdf_file_path, 'rb') as file:
        pdf_data = file.read()
        msg.add_attachment(pdf_data, maintype='application', subtype='pdf')

    # Connect to Gmail's SMTP server
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(GMAIL, GMAIL_PASSWORD)
        smtp.send_message(msg)


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        # if not username:
        #     # Handle the case where the username is empty or not provided in the form
        #     context = {'message': 'Please provide a username'}
        #     return render(request, 'invoices/signup.html', context)

        user = User.objects.filter(username=username)
        # print(user)
        if user:
            context = {'message': 'User already registered'}
            return render(request, 'invoice/signup.html', context)
        else:
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            context = {'message': 'User registered'}
            return render(request, 'invoice/signup.html', context)
    return render(request, 'invoice/signup.html')

    # return render(request, 'invoices/signup.html')


def sign(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()
        if user is None:
            context = {'message': 'User does not registered'}
            return render(request, 'invoice/signin.html', context)
        else:
            user = authenticate(username=username, password=password)
        if user is None:
            context = {'message': 'wrong password'}
            return render(request, 'invoice/signin.html', context)
        else:
            login(request, user)
            base(request)
            return redirect('/adminpanel/')
    return render(request, 'invoice/signin.html')


import stripe
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import Profile  # Make sure to import the Profile model or adjust the import statement accordingly

@login_required(login_url='/signin/')
def sub(request):
    if request.method == 'POST':
        membership = request.POST.get('plan')
        amount = 20

        if membership == 'YEARLY':
            amount = 100

        print(membership)

        stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

        customer = stripe.Customer.create(
            email=request.user.email,
            source=request.POST['stripeToken']
        )

        print(customer)

        currency = 'zar'  # Set the currency to South African Rand (ZAR)

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount * 100,
            currency=currency,
            description="plan"
        )

        if charge['paid'] == True:
            user = request.user
            profile, created = Profile.objects.get_or_create(user=user)

            if charge['amount'] == 10000:
                profile.subscription_type = 'Y'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(days=365)
                profile.pro_expiry_date = expiry
                profile.save()

            elif charge['amount'] == 2000:
                profile.subscription_type = 'M'
                profile.is_pro = True
                expiry = datetime.now() + timedelta(days=30)
                profile.pro_expiry_date = expiry
                profile.save()

            return redirect('invoice/charge/')

    return render(request, 'invoice/subscrib.html')


def charge(request):
    return render(request, 'invoice/charge.html')

def checkpdf(request,  pk):
    try:
        invoice = Invoice.objects.get(id=pk)
        # Perform actions like deletion or other operations here if needed
        # invoice.delete()
        # return redirect('success_url')  # Replace 'success_url' with the URL you want to redirect to after successful deletion
    except Invoice.DoesNotExist:
        # If the invoice with the specified id does not exist, you can redirect to a different URL
        return redirect('view_invoice')
        # Assuming 'pdf_filename' is the field storing the path to the PDF file in your 'Invoice' model
    pdf_filename = invoice # Replace 'pdf_filename' with the actual attribute in your model

    # Constructing the full path to the PDF file
    pdf_path = os.path.join(settings.BASE_DIR, 'invoice', 'templates', 'invoice', 'pdfs', str(pdf_filename))

    try:
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{pdf_filename}"'
            return response
    except FileNotFoundError:
        return HttpResponse("PDF file not found", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)

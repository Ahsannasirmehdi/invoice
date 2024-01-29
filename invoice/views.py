from datetime import datetime, timedelta
import uuid
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, FileResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.sessions.models import Session
from django.views.decorators.cache import never_cache
from utils.filehandler import handle_file_upload
from django.shortcuts import render, redirect
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
import stripe
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from .models import Profile  # Make sure to import the Profile model or adjust the import statement accordingly
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

@never_cache
def schedule(request):
    return render(request, "invoice/schedule.html")
@never_cache
def  resetpasswordview(request):
    if request.method == "POST":
        content = request.POST.get('username')
        email = request.POST.get('password')
        user=User.objects.filter(username=content).first()
        print(user)
        if user is None:
            context = {'message': 'User found'}
            return render(request, 'invoice/passreset.html', context)
        else:
            u = User.objects.get(username=content)
            u.set_password(str(email))
            u.save()
            return redirect("/complete/")
    return  render(request,'invoice/passreset.html')
@never_cache
def  resetpasswordcomplete(request):

    return  render(request,'invoice/complete.html')
@never_cache
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
@never_cache
def home(requests):
    return  render(requests,'invoice/index.html')

# Modify your existing sub function to call the generate_invoices task


@never_cache
def delete_all_invoice(request):
    # Delete all invoice
    if request.method == "POST":
        Invoice.objects.all().delete()
        return redirect('view_invoice')

    return render(request, "invoice/del.html")

@never_cache
def adin(request):
    return render(request, "invoice/admin.html")

@never_cache
def addata(request):
    n = Profile.objects.all()
    context = {'profiles': n}
    return render(request, "invoice/admindata.html", context)
@never_cache
def registerusers(request):
    n = User.objects.all()
    context = {'profiles': n}
    return render(request, "invoice/regusers.html", context)










@never_cache
def create_invoice(request):

    form = InvoiceForm()

    if request.method == "POST":

        form = InvoiceForm(request.POST)
        user = request.user
        if form.is_valid():
            print('ew')
            content = request.POST.get('content')
            email = request.POST.get('email')
            invoice = Invoice.objects.create(
                user=user,
                customer=form.cleaned_data.get("customer"),
                contact=form.cleaned_data.get("contact"),
                email=form.cleaned_data.get("email"),
                comments=form.cleaned_data.get("comments"),
                date=form.cleaned_data.get("date"),
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

@never_cache
def template(request):
    return render(request, 'invoice/custom/new.html')

@never_cache
def view_invoice(request):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        return redirect('/home/')

    # Query the database only if the user is authenticated
    invoice = Invoice.objects.filter(user=request.user)

    context = {
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
# @never_cache
# def view_invoice_detail(request, pk):
#
#     # total_customer = Customer.objects.count()
#     total_invoice = Invoice.objects.count()
#     # total_income = getTotalIncome()
#
#     invoice = Invoice.objects.get(id=pk)
#
#
#     context = {
#
#         # "total_customer": total_customer,
#         "total_invoice": total_invoice,
#         # "total_income": total_income,
#         # 'invoice': invoice,
#
#     }
#
#     return render(request, "invoice/view_invoice_detail.html", context)


# Delete invoice
@never_cache
def delete_invoice(request, pk):

    # total_customer = Customer.objects.count()
    total_invoice = Invoice.objects.count()
    try:
        invoice = Invoice.objects.get(id=pk)
    except Invoice.DoesNotExist:
     # If the invoice with the specified id does not exist, you can redirect to a different URL
        return redirect('view_invoice')

    if request.method == "POST":

        invoice.delete()
        return redirect("view_invoice")

    context = {

        # "total_customer": total_customer,
        "total_invoice": total_invoice,

        "invoice": invoice,

    }

    return render(request, "invoice/delete_invoice.html", context)




@never_cache
def edit_invoice(request, pk):
    invoice = get_object_or_404(Invoice, id=pk)


    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)


        if form.is_valid() :
            form.save()


    else:
        form = InvoiceForm(instance=invoice)


    context = {
        "form": form,

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

@never_cache
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

@never_cache
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
            return redirect('/mainpage/')
    return render(request, 'invoice/signin.html')

@never_cache
def sign1(request):
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
            return redirect('/subscribe/')
    return render(request, 'invoice/signin.html')
@login_required(login_url='/purchasesignin/')
def sub(request):
    if request.method == 'POST':
        membership = request.POST.get('plan')
        amount = 20

        if membership == 'YEARLY':
            amount = 100



        stripe.api_key = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'

        customer = stripe.Customer.create(
            email=request.user.email,
            source=request.POST['stripeToken']
        )



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

            return redirect('/charge/')

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

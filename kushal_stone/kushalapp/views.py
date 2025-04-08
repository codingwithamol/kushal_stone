from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')
        user = CustomUser.objects.create_user(username=username, email=email, password=password, role='Admin')
        messages.success(request, 'Admin registered successfully')
        return redirect('login')
    return render(request, 'signup.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()  # Ensure you are using the correct user model

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        print(f"Attempting login: Username={username}, Password={password}")  # Debugging

        user = authenticate(request, username=username, password=password)

        if user:
            print(f"Authenticated User: {user.username} - {user.role}")  # Debugging
            login(request, user)

            # Redirect based on user role
            role = user.role.lower()  # Ensure lowercase match
            return redirect(reverse(f'{role}_dashboard'))
        else:
            print("Authentication failed")  # Debugging
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@login_required
def sales_dashboard(request):
    return render(request, 'sales_dashboard.html')

@login_required
def operations_dashboard(request):
    return render(request, 'operations_dashboard.html')

@login_required
def manager_dashboard(request):
    return render(request, 'manager_dashboard.html')

@login_required
def finance_dashboard(request):
    return render(request, 'finance_dashboard.html')

def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        role = request.POST['role']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('create_user')
        if CustomUser.objects.filter(mobile_number=mobile, role=role).exists():
            messages.error(request, 'User with this mobile number and role already exists')
            return redirect('create_user')
        user = CustomUser.objects.create_user(username=email, email=email, password=password, mobile_number=mobile, role=role)
        messages.success(request, 'User created successfully')
        return redirect('admin_dashboard')
    return render(request, 'create_user.html')




from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Service

def is_admin_user(user):
    return user.is_authenticated and user.role == 'Admin'

@login_required
@user_passes_test(is_admin_user)
def requirements_dashboard(request):
    products = Product.objects.all()
    services = Service.objects.all()

    if request.method == 'POST':
        if 'add_product' in request.POST:
            name = request.POST.get('product_name')
            if name:
                Product.objects.create(name=name)
                messages.success(request, 'Product added successfully.')
                return redirect('requirements_dashboard')

        elif 'add_service' in request.POST:
            name = request.POST.get('service_name')
            if name:
                Service.objects.create(name=name)
                messages.success(request, 'Service added successfully.')
                return redirect('requirements_dashboard')

    return render(request, 'requirements_dashboard.html', {
        'products': products,
        'services': services,
    })
@login_required
@user_passes_test(is_admin_user)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('requirements_dashboard')

@login_required
@user_passes_test(is_admin_user)
def delete_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    service.delete()
    return redirect('requirements_dashboard')

@login_required
@user_passes_test(is_admin_user)
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        new_name = request.POST.get('product_name')
        if new_name:
            product.name = new_name
            product.save()
            return redirect('requirements_dashboard')
    return render(request, 'edit_product.html', {'product': product})

@login_required
@user_passes_test(is_admin_user)
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        new_name = request.POST.get('service_name')
        if new_name:
            service.name = new_name
            service.save()
            return redirect('requirements_dashboard')
    return render(request, 'edit_service.html', {'service': service})





# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Product, Service, Lead, CustomUser
from django.contrib.auth.decorators import login_required


@login_required
def add_lead(request):
    products = Product.objects.all()
    services = Service.objects.all()
    sales_persons = CustomUser.objects.filter(role='Sales')  # corrected
    follow_up_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        data = request.POST
        errors = {}

        required_fields = [
            'full_name', 'mobile_number', 'email', 'requirements',
            'address', 'architect_name', 'architect_number',
            'source', 'enquiry_date', 'sales_person',
            'customer_segment', 'follow_up_date', 'follow_up_person'
        ]

        for field in required_fields:
            if not data.get(field):
                errors[field] = "This field can't be empty."

        if data.get('source') == 'Other' and not data.get('source_other'):
            errors['source_other'] = "Please specify other source."

        if errors:
            return render(request, 'add_lead.html', {
                'products': products,
                'services': services,
                'sales_persons': sales_persons,
                'follow_up_persons': follow_up_persons,
                'errors': errors,
                'data': data
            })

        lead = Lead.objects.create(
            full_name=data['full_name'],
            mobile_number=data['mobile_number'],
            email=data['email'],
            requirements=data['requirements'],
            address=data['address'],
            architect_name=data['architect_name'],
            architect_number=data['architect_number'],
            source=data['source'],
            source_other=data.get('source_other'),
            enquiry_date=data['enquiry_date'],
            sales_person_id=data['sales_person'],
            customer_segment=data['customer_segment'],
            follow_up_date=data['follow_up_date'],
            follow_up_person_id=data['follow_up_person']
        )

        if data['requirements'] == 'products':
            lead.products.set(data.getlist('products'))
        elif data['requirements'] == 'services':
            lead.services.set(data.getlist('services'))
        else:
            lead.products.set(data.getlist('products'))
            lead.services.set(data.getlist('services'))

        messages.success(request, 'Lead added successfully!')
        return redirect('view_leads')

    return render(request, 'add_lead.html', {
        'products': products,
        'services': services,
        'sales_persons': sales_persons,
        'follow_up_persons': follow_up_persons
    })


@login_required
def view_leads(request):
    leads = Lead.objects.all()
    return render(request, 'view_leads.html', {'leads': leads})

# @login_required
# def edit_lead(request, pk):
#     lead = get_object_or_404(Lead, pk=pk)
#     products = Product.objects.all()
#     services = Service.objects.all()
#     sales_persons = CustomUser.objects.filter(role='Sales')

#     if request.method == 'POST':
#         data = request.POST
#         lead.full_name = data['full_name']
#         lead.mobile_number = data['mobile_number']
#         lead.email = data['email']
#         lead.requirements = data['requirements']
#         lead.address = data['address']
#         lead.architect_name = data['architect_name']
#         lead.architect_number = data['architect_number']
#         lead.source = data['source']
#         lead.source_other = data.get('source_other')
#         lead.enquiry_date = data['enquiry_date']
#         lead.sales_person_id = data['sales_person']
#         lead.customer_segment = data['customer_segment']
#         lead.follow_up_date = data['follow_up_date']
#         lead.follow_up_person_id = data['follow_up_person']
#         lead.save()

#         if data['requirements'] == 'products':
#             lead.products.set(data.getlist('products'))
#             lead.services.clear()
#         elif data['requirements'] == 'services':
#             lead.services.set(data.getlist('services'))
#             lead.products.clear()
#         else:
#             lead.products.set(data.getlist('products'))
#             lead.services.set(data.getlist('services'))

#         messages.success(request, 'Lead updated successfully!')
#         return redirect('view_leads')

#     return render(request, 'edit_lead.html', {
#         'lead': lead,
#         'products': products,
#         'services': services,
#         'sales_persons': sales_persons
#     })

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

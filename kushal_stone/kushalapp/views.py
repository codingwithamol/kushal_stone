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




# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Lead, CustomUser, FollowUp1

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Lead

@login_required
def my_work(request):
    # Directly assigned leads (not closed)
    direct_leads = Lead.objects.filter(follow_up_person=request.user, is_closed=False)

    # Leads assigned as next follow-up in FollowUp1, but not closed
    followup1_leads = Lead.objects.filter(followup1__next_followup_person=request.user, is_closed=False)

    # Combine and remove duplicates
    leads = direct_leads.union(followup1_leads)

    lead_data = []

    for lead in leads:
        status = ""
        followup_date = None

        if not hasattr(lead, 'followup1'):
            status = {'label': '1st Follow Up', 'url_name': 'follow_up_1'}
        elif not hasattr(lead, 'followup2'):
            followup_date = lead.followup1.next_followup_date
            status = {'label': '2nd Follow Up', 'url_name': 'follow_up_2'}
        elif not hasattr(lead, 'followup3'):
            followup_date = lead.followup2.next_followup_date
            status = {'label': '3rd Follow Up', 'url_name': 'follow_up_3'}
        elif not hasattr(lead, 'followup4'):
            followup_date = lead.followup3.next_followup_date
            status = {'label': '4th Follow Up', 'url_name': 'follow_up_4'}
        else:
            followup_date = lead.followup4.next_followup_date
            close_status = lead.followup4.close_status
            status = {'label': f'Closed ({close_status})', 'url_name': None}

        lead_data.append({
            'lead': lead,
            'status': status,
            'followup_date': followup_date
        })

    return render(request, 'my_work.html', {'lead_data': lead_data})


@login_required
def completed_follow_up(request):
    # Leads that this user was previously responsible for but are now assigned to someone else
    past_leads = Lead.objects.filter(
        followup1__user=request.user
    ).exclude(followup1__next_followup_person=request.user)

    return render(request, 'completed_follow_up.html', {'lead_data': past_leads})


# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Lead, CustomUser, FollowUp1, FollowUp2, FollowUp3, FollowUp4, FollowUp5, FollowUp6, FollowUp7, FollowUp8, FollowUp9, FollowUp10
from django.contrib.auth import get_user_model
User = get_user_model()


@login_required
def follow_up_1(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if hasattr(lead, 'followup1'):
        return redirect('follow_up_2', lead_id=lead_id)

    if request.method == 'POST':
        followup = FollowUp1(
            lead=lead,
            customer_visited=request.POST.get('customer_visited') == 'yes',
            inspection_done=request.POST.get('inspection_done') == 'yes',
            quotation_given=request.POST.get('quotation_given') == 'yes',
            quotation_amount=request.POST.get('quotation_amount') or None,
            description=request.POST.get('description'),
            quotation_file=request.FILES.get('quotation_file'),
            next_followup_date=request.POST.get('next_followup_date'),
        )

        user_id = request.POST.get('next_followup_person')
        if user_id:
            followup.next_followup_person = CustomUser.objects.get(id=user_id)

        followup.save()

        # OPTIONAL: Transfer the lead assignment (if you want to)
        # lead.follow_up_person = followup.next_followup_person
        # lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_1.html', {
        'lead': lead,
        'sales_persons': sales_persons,
    })



@login_required
def follow_up_2(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')  # Or use your role logic

    if hasattr(lead, 'followup2'):
        return redirect('my_work')

    if request.method == 'POST':
        followup = FollowUp2()
        followup.lead = lead
        followup.next_followup_date = request.POST.get('next_followup_date')
        followup.remarks = request.POST.get('remarks')
        followup.lead_type = request.POST.get('lead_type')

        # Handle reassignment
        next_user_id = request.POST.get('third_followup_person')
        if next_user_id:
            next_user = CustomUser.objects.get(id=next_user_id)
            followup.next_followup_person = next_user

        # Handle close lead
        if request.POST.get('close_status'):
            followup.close_status = 'Win'  # Or 'Loss' based on UI
            lead.is_closed = True
            lead.save()
        else:
            followup.close_status = 'Open'

        followup.save()

        # 🚨 This ensures the current user doesn't see this lead anymore
        # because `my_work` will now show it for the newly assigned person

        return redirect('my_work')

    return render(request, 'follow_up_2.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })




@login_required
def follow_up_3(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if hasattr(lead, 'followup3'):
        return redirect('follow_up_4', lead_id=lead_id)
    if request.method == 'POST':
        followup = FollowUp3()
        followup.lead = lead
        followup.fourth_followup_date = request.POST.get('fourth_followup_date')
        followup.fourth_followup_person_id = request.POST.get('fourth_followup_person')
        followup.lead_type = request.POST.get('lead_type')
        followup.remarks = request.POST.get('remarks')
        followup.close_status = request.POST.get('close_status')
        followup.save()
        return redirect('my_work') if followup.close_status else redirect('follow_up_4', lead_id=lead_id)
    return render(request, 'follow_up_3.html', {'lead': lead})

@login_required
def follow_up_4(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if hasattr(lead, 'followup4'):
        return redirect('follow_up_5', lead_id=lead_id)
    if request.method == 'POST':
        followup = FollowUp4()
        followup.lead = lead
        followup.fifth_followup_date = request.POST.get('fifth_followup_date')
        followup.fifth_followup_person_id = request.POST.get('fifth_followup_person')
        followup.lead_type = request.POST.get('lead_type')
        followup.remarks = request.POST.get('remarks')
        followup.close_status = request.POST.get('close_status')
        followup.save()
        return redirect('my_work') if followup.close_status else redirect('follow_up_5', lead_id=lead_id)
    return render(request, 'follow_up_4.html', {'lead': lead})

@login_required
def follow_up_5(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if hasattr(lead, 'followup5'):
        return redirect('follow_up_6', lead_id=lead_id)
    if request.method == 'POST':
        followup = FollowUp5()
        followup.lead = lead
        followup.sixth_followup_date = request.POST.get('sixth_followup_date')
        followup.sixth_followup_person_id = request.POST.get('sixth_followup_person')
        followup.lead_type = request.POST.get('lead_type')
        followup.remarks = request.POST.get('remarks')
        followup.close_status = request.POST.get('close_status')
        followup.save()
        return redirect('my_work') if followup.close_status else redirect('follow_up_6', lead_id=lead_id)
    return render(request, 'follow_up_5.html', {'lead': lead})

@login_required
def follow_up_6(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if hasattr(lead, 'followup6'):
        return redirect('follow_up_7', lead_id=lead_id)
    if request.method == 'POST':
        followup = FollowUp6()
        followup.lead = lead
        followup.seventh_followup_date = request.POST.get('seventh_followup_date')
        followup.seventh_followup_person_id = request.POST.get('seventh_followup_person')
        followup.lead_type = request.POST.get('lead_type')
        followup.remarks = request.POST.get('remarks')
        followup.close_status = request.POST.get('close_status')
        followup.save()
        return redirect('my_work') if followup.close_status else redirect('follow_up_7', lead_id=lead_id)
    return render(request, 'follow_up_6.html', {'lead': lead})

@login_required
def follow_up_7(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if hasattr(lead, 'followup7'):
        return redirect('follow_up_8', lead_id=lead_id)
    if request.method == 'POST':
        followup = FollowUp7()
        followup.lead = lead
        followup.eighth_followup_date = request.POST.get('eighth_followup_date')
        followup.eighth_followup_person_id = request.POST.get('eighth_followup_person')
        followup.lead_type = request.POST.get('lead_type')
        followup.remarks = request.POST.get('remarks')
        followup.close_status = request.POST.get('close_status')
        followup.save()
        return redirect('my_work') if followup.close_status else redirect('follow_up_8', lead_id=lead_id)
    return render(request, 'follow_up_7.html', {'lead': lead})

@login_required
def follow_up_8(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if hasattr(lead, 'followup8'):
        return redirect('follow_up_9', lead_id=lead_id)
    if request.method == 'POST':
        followup = FollowUp8()
        followup.lead = lead
        followup.ninth_followup_date = request.POST.get('ninth_followup_date')
        followup.ninth_followup_person_id = request.POST.get('ninth_followup_person')
        followup.lead_type = request.POST.get('lead_type')
        followup.remarks = request.POST.get('remarks')
        followup.close_status = request.POST.get('close_status')
        followup.save()
        return redirect('my_work') if followup.close_status else redirect('follow_up_9', lead_id=lead_id)
    return render(request, 'follow_up_8.html', {'lead': lead})

@login_required
def follow_up_9(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if hasattr(lead, 'followup9'):
        return redirect('follow_up_10', lead_id=lead_id)
    if request.method == 'POST':
        followup = FollowUp9()
        followup.lead = lead
        followup.tenth_followup_date = request.POST.get('tenth_followup_date')
        followup.tenth_followup_person_id = request.POST.get('tenth_followup_person')
        followup.lead_type = request.POST.get('lead_type')
        followup.remarks = request.POST.get('remarks')
        followup.close_status = request.POST.get('close_status')
        followup.save()
        return redirect('my_work') if followup.close_status else redirect('follow_up_10', lead_id=lead_id)
    return render(request, 'follow_up_9.html', {'lead': lead})

@login_required
def follow_up_10(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    if hasattr(lead, 'followup10'):
        return redirect('my_work')
    if request.method == 'POST':
        followup = FollowUp10()
        followup.lead = lead
        followup.eleventh_followup_date = request.POST.get('eleventh_followup_date')
        followup.eleventh_followup_person_id = request.POST.get('eleventh_followup_person')
        followup.lead_type = request.POST.get('lead_type')
        followup.remarks = request.POST.get('remarks')
        followup.close_status = request.POST.get('close_status')
        followup.save()
        return redirect('my_work')
    return render(request, 'follow_up_10.html', {'lead': lead})


from django.contrib import messages

from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Lead

from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from .models import Lead

@require_POST
def close_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    # Set is_closed to True
    lead.is_closed = True

    # Determine win or lose
    status = request.POST.get('win_status')
    if status == 'win':
        lead.win_status = True
    else:
        lead.win_status = False

    lead.save()
    return redirect('my_work')  # or wherever you want to go


@login_required
def assign_lead(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    
    if request.method == 'POST':
        new_user_id = request.POST.get('new_assignee')
        if new_user_id:
            new_user = get_object_or_404(CustomUser, id=new_user_id)
            lead.follow_up_person = new_user
            lead.save()
            messages.success(request, f"Lead reassigned to {new_user.username}.")
    
    return redirect('my_work')



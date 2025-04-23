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









# def get_latest_followup_type(lead):
#     for model in [FollowUp10, FollowUp9, FollowUp8, FollowUp7, FollowUp6, FollowUp5, FollowUp4, FollowUp3, FollowUp2, FollowUp1]:
#         followup = model.objects.filter(lead=lead).first()
#         if followup:
#             return followup.lead_type, followup.close_status
#     return None, None




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Lead
from .models import (
    FollowUp1, FollowUp2, FollowUp3, FollowUp4,
    FollowUp5, FollowUp6, FollowUp7, FollowUp8,
    FollowUp9, FollowUp10, FollowUpBase
)

@login_required
def sales_dashboard(request):
    total_leads = Lead.objects.count()
    completed_leads = Lead.objects.filter(is_closed=True).count()
    my_work_total = Lead.objects.filter(sales_person=request.user).count()

    # Get selected follow-up model based on query param
    follow_up_type = request.GET.get('follow_up_type', 'FollowUp1')
    follow_up_model = globals().get(follow_up_type, FollowUp1)

    # Lead type counts from selected follow-up
    # lead_types = follow_up_model.objects.values('lead_type').annotate(count=Count('lead_type'))
    # lead_type_labels = [entry['lead_type'] for entry in lead_types]
    # lead_type_counts = [entry['count'] for entry in lead_types]

    # Win/Loss Status
    win_loss = Lead.objects.filter(is_closed=True).values('win_status').annotate(count=Count('win_status'))
    win_loss_labels = ['Win' if entry['win_status'] else 'Loss' for entry in win_loss]
    win_loss_counts = [entry['count'] for entry in win_loss]

    # Customer Segment
    customer_segments = Lead.objects.values('customer_segment').annotate(count=Count('customer_segment'))
    customer_segment_labels = [entry['customer_segment'] for entry in customer_segments]
    customer_segment_counts = [entry['count'] for entry in customer_segments]

    # Lead Source
    sources = Lead.objects.values('source').annotate(count=Count('source'))
    source_labels = [entry['source'] for entry in sources]
    source_counts = [entry['count'] for entry in sources]

    context = {
        'total_leads': total_leads,
        'completed_leads': completed_leads,
        'my_work_total': my_work_total,
        # 'lead_type_labels': lead_type_labels,
        # 'lead_type_counts': lead_type_counts,
        'win_loss_labels': win_loss_labels,
        'win_loss_counts': win_loss_counts,
        'customer_segment_labels': customer_segment_labels,
        'customer_segment_counts': customer_segment_counts,
        'source_labels': source_labels,
        'source_counts': source_counts,
        'follow_up_type': follow_up_type
    }

    return render(request, 'sales_dashboard.html', context)






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
            'customer_segment', 'next_followup_date', 'follow_up_person'
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
            next_followup_date=data['next_followup_date'],
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
from django.utils import timezone
from datetime import datetime, time, date


@login_required
def my_work(request):
    user = request.user
    leads = Lead.objects.filter(is_closed=False).distinct()
    lead_data = []

    for lead in leads:
        status = None
        followup_date = None
        assigned_to_user = False

        # 1st Follow-Up
        if not hasattr(lead, 'followup1'):
            if lead.follow_up_person == user:
                status = {'label': '1st Follow Up', 'url_name': 'follow_up_1'}
                assigned_to_user = True

        # 2nd Follow-Up
        elif not hasattr(lead, 'followup2'):
            f1 = lead.followup1
            if f1.next_followup_person == user:
                followup_date = f1.next_followup_date
                status = {'label': '2nd Follow Up', 'url_name': 'follow_up_2'}
                assigned_to_user = True

        # 3rd Follow-Up
        elif not hasattr(lead, 'followup3'):
            f2 = lead.followup2
            if f2.next_followup_person == user:
                followup_date = f2.next_followup_date
                status = {'label': '3rd Follow Up', 'url_name': 'follow_up_3'}
                assigned_to_user = True

        # 4th Follow-Up
        elif not hasattr(lead, 'followup4'):
            f3 = lead.followup3
            if f3.next_followup_person == user:
                followup_date = f3.next_followup_date
                status = {'label': '4th Follow Up', 'url_name': 'follow_up_4'}
                assigned_to_user = True

        # 5th Follow-Up
        elif not hasattr(lead, 'followup5'):
            f4 = lead.followup4
            if f4.next_followup_person == user:
                followup_date = f4.next_followup_date
                status = {'label': '5th Follow Up', 'url_name': 'follow_up_5'}
                assigned_to_user = True

        # 6th Follow-Up
        elif not hasattr(lead, 'followup6'):
            f5 = lead.followup5
            if f5.next_followup_person == user:
                followup_date = f5.next_followup_date
                status = {'label': '6th Follow Up', 'url_name': 'follow_up_6'}
                assigned_to_user = True

        # 7th Follow-Up
        elif not hasattr(lead, 'followup7'):
            f6 = lead.followup6
            if f6.next_followup_person == user:
                followup_date = f6.next_followup_date
                status = {'label': '7th Follow Up', 'url_name': 'follow_up_7'}
                assigned_to_user = True

        # 8th Follow-Up
        elif not hasattr(lead, 'followup8'):
            f7 = lead.followup7
            if f7.next_followup_person == user:
                followup_date = f7.next_followup_date
                status = {'label': '8th Follow Up', 'url_name': 'follow_up_8'}
                assigned_to_user = True

        # 9th Follow-Up
        elif not hasattr(lead, 'followup9'):
            f8 = lead.followup8
            if f8.next_followup_person == user:
                followup_date = f8.next_followup_date
                status = {'label': '9th Follow Up', 'url_name': 'follow_up_9'}
                assigned_to_user = True

        # 10th Follow-Up
        elif not hasattr(lead, 'followup10'):
            f9 = lead.followup9
            if f9.next_followup_person == user:
                followup_date = f9.next_followup_date
                status = {'label': '10th Follow Up', 'url_name': 'follow_up_10'}
                assigned_to_user = True

        # Lead Closed (after 10th follow-up)
        else:
            f10 = lead.followup10
            followup_date = f10.next_followup_date
            close_status = getattr(f10, 'close_status', 'Closed')
            status = {'label': f'Closed ({close_status})', 'url_name': None}
            # Skipping adding this to lead_data unless you want to display closed leads

        if assigned_to_user:
            lead_data.append({
                'lead': lead,
                'status': status,
                'followup_date': followup_date
            })


    lead_data.sort(
        key=lambda x: (
        datetime.combine(x['followup_date'], time.min)
        if isinstance(x['followup_date'], date) and not isinstance(x['followup_date'], datetime)
        else x['followup_date'] or datetime.max
    )
)

    return render(request, 'my_work.html', {'lead_data': lead_data})



from django.shortcuts import render, get_object_or_404
from .models import Lead, FollowUp1, FollowUp2, FollowUp3, FollowUp4, FollowUp5, FollowUp6, FollowUp7, FollowUp8, FollowUp9, FollowUp10

def work_history(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    followups = []
    followup_models = [FollowUp1, FollowUp2, FollowUp3, FollowUp4, FollowUp5, FollowUp6, FollowUp7, FollowUp8, FollowUp9, FollowUp10]

    for model in followup_models:
        try:
            followup = model.objects.get(lead=lead)
        except model.DoesNotExist:
            followup = None
        followups.append(followup)

    return render(request, 'work_history.html', {
        'lead': lead,
        'followups': followups,
    })


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
        customer_visited = request.POST.get('customer_visited') == 'yes'
        inspection_done = request.POST.get('inspection_done') == 'yes'
        quotation_given = request.POST.get('quotation_given') == 'yes'
        quotation_amount = request.POST.get('quotation_amount') or None
        description = request.POST.get('description')
        quotation_file = request.FILES.get('quotation_file')
        lead_type = request.POST.get('lead_type')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'loss'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'loss':
                close_status = 'Loss'
        else:
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp1 record
        FollowUp1.objects.create(
            lead=lead,
            customer_visited=customer_visited,
            inspection_done=inspection_done,
            quotation_given=quotation_given,
            quotation_amount=quotation_amount,
            description=description,
            quotation_file=quotation_file,
            lead_type=lead_type,
            followup_person=request.user,
            next_followup_date=next_followup_date if close_lead != 'yes' else None,
            next_followup_person=next_followup_person if close_lead != 'yes' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.closed_by = request.user
            lead.save()
        else:
            # Assign next followup person
            if next_followup_person:
                lead.follow_up_person = next_followup_person
                lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_1.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })



from django.shortcuts import render, get_object_or_404, redirect
from .models import Lead, FollowUp2, CustomUser
from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Lead, FollowUp2, CustomUser

@login_required
def follow_up_2(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get followup fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp3 entry
        FollowUp2.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.closed_by = request.user  # <-- add this line

            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_2.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })



@login_required
def follow_up_3(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get followup fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp3 entry
        FollowUp3.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_3.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Lead, FollowUp4, CustomUser  # Make sure FollowUp4 model exists

@login_required
def follow_up_4(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp4.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_4.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })



@login_required
def follow_up_5(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp5.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_5.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })





@login_required
def follow_up_6(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp6.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_6.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })


@login_required
def follow_up_7(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp7.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_7.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })


@login_required
def follow_up_8(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp8.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_8.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })



@login_required
def follow_up_9(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None
        next_followup_date = None
        next_followup_person = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open - get follow-up fields
            close_status = 'Open'
            next_followup_date = request.POST.get('next_followup_date')
            next_followup_person_id = request.POST.get('next_followup_person')
            next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        # Create FollowUp4 entry
        FollowUp9.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date if close_lead == 'no' else None,
            next_followup_person=next_followup_person if close_lead == 'no' else None,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_9.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })



@login_required
def follow_up_10(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)
    sales_persons = CustomUser.objects.filter(role='Sales')

    if request.method == 'POST':
        lead_type = request.POST.get('lead_type')
        remarks = request.POST.get('remarks')
        close_lead = request.POST.get('close_lead')
        win_status = request.POST.get('win_status')  # 'win' or 'lose'

        close_status = None

        if close_lead == 'yes':
            # Closed lead
            if win_status == 'win':
                close_status = 'Win'
            elif win_status == 'lose':
                close_status = 'Loss'
        else:
            # Still open
            close_status = 'Open'

        # Create FollowUp10 entry (no next follow-up fields)
        FollowUp10.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            close_status=close_status
        )

        # Update lead if it's closed
        if close_status in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
            lead.save()

        return redirect('my_work')

    return render(request, 'follow_up_10.html', {
        'lead': lead,
        'sales_persons': sales_persons
    })

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

#close lead function
@login_required
def closed_leads(request):
    closed = Lead.objects.filter(is_closed=True, follow_up_person=request.user)
    return render(request, 'close_lead.html', {'closed_leads': closed})


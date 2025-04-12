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
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Lead
from .models import FollowUp1, FollowUp2, FollowUp3, FollowUp4 , FollowUp5, FollowUp6 , FollowUp7 , FollowUp8 , FollowUp9 , FollowUp10 , FollowUpBase

@login_required
def sales_dashboard(request):
    user = request.user

    total_leads = Lead.objects.count()
    completed_leads = Lead.objects.filter(is_closed=True).count()
    my_work_total = Lead.objects.filter(follow_up_person=user, is_closed=False).count()

    # Initialize lead type data
    lead_types = ['Hot', 'Warm', 'Cold', 'Not Interested']
    lead_type_data = {lt: 0 for lt in lead_types}

    for model in [FollowUp1, FollowUp2, FollowUp3, FollowUp4]:
        qs = model.objects.values('lead_type').annotate(count=Count('id'))
        for entry in qs:
            lead_type = entry['lead_type']
            if lead_type in lead_type_data:
                lead_type_data[lead_type] += entry['count']

    # Prepare lists for chart
    lead_type_labels = list(lead_type_data.keys())
    lead_type_counts = list(lead_type_data.values())

    context = {
        'total_leads': total_leads,
        'completed_leads': completed_leads,
        'my_work_total': my_work_total,
        'lead_type_labels': lead_type_labels,
        'lead_type_counts': lead_type_counts,
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

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Lead

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

        # Lead Closed
        else:
            f4 = lead.followup4
            followup_date = f4.next_followup_date
            close_status = f4.close_status
            status = {'label': f'Closed ({close_status})', 'url_name': None}
            # No need to assign it, just show if needed (currently skipping closed leads)

        if assigned_to_user:
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
        is_closing = 'close_lead' in request.POST

        followup = FollowUp1(
            lead=lead,
            customer_visited=request.POST.get('customer_visited') == 'yes',
            inspection_done=request.POST.get('inspection_done') == 'yes',
            quotation_given=request.POST.get('quotation_given') == 'yes',
            quotation_amount=request.POST.get('quotation_amount') or None,
            description=request.POST.get('description'),
            quotation_file=request.FILES.get('quotation_file'),
            next_followup_date=None if is_closing else request.POST.get('next_followup_date'),
            lead_type=request.POST.get('lead_type'),
            followup_person=request.user,
        )

        if is_closing:
            lead.is_closed = True
            win_status = request.POST.get("win_status")
            if win_status == "win":
                lead.win_status = True
                followup.close_status = "Win"
            elif win_status == "loss":
                lead.win_status = False
                followup.close_status = "Loss"
            lead.save()
        else:
            user_id = request.POST.get('next_followup_person')
            if user_id:
                next_person = CustomUser.objects.get(id=user_id)
                followup.next_followup_person = next_person
                lead.follow_up_person = next_person
                lead.save()

        followup.save()
        return redirect('my_work')

    return render(request, 'follow_up_1.html', {
        'lead': lead,
        'sales_persons': sales_persons,
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
        next_followup_date = request.POST.get('next_followup_date')
        next_followup_person_id = request.POST.get('next_followup_person')
        next_followup_person = CustomUser.objects.get(id=next_followup_person_id) if next_followup_person_id else None

        win_status = request.POST.get('win_status')  # 'win' or 'lose'
        close_status = None

        if win_status == 'win':
            close_status = 'Win'
        elif win_status == 'lose':
            close_status = 'Loss'

        # Create FollowUp2 entry
        followup2 = FollowUp2.objects.create(
            lead=lead,
            followup_person=request.user,
            lead_type=lead_type,
            remarks=remarks,
            next_followup_date=next_followup_date,
            next_followup_person=next_followup_person,
            close_status=close_status if close_status else 'Open'
        )

        # If closed, update lead
        if close_status:
            lead.is_closed = True
            lead.win_status = True if close_status == 'Win' else False
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

    if hasattr(lead, 'followup3'):
        return redirect('follow_up_4', lead_id=lead_id)

    if request.method == 'POST':
        followup = FollowUp3(
            lead=lead,
            fourth_followup_date=request.POST.get('fourth_followup_date'),
            lead_type=request.POST.get('lead_type'),
            remarks=request.POST.get('remarks'),
            close_status=request.POST.get('close_status') or 'Open',
        )

        fourth_user_id = request.POST.get('fourth_followup_person')
        if fourth_user_id:
            try:
                next_user = CustomUser.objects.get(id=fourth_user_id)
                followup.fourth_followup_person = next_user

                # 🔁 Assign new person to the lead
                lead.follow_up_person = next_user
                lead.save()
            except CustomUser.DoesNotExist:
                pass  # You could also log this or return an error message

        # ✅ If lead is closed, update status
        if request.POST.get('close_status') in ['Win', 'Loss']:
            lead.is_closed = True
            lead.win_status = True if request.POST.get('close_status') == 'Win' else False
            lead.save()

        followup.save()

        # Redirect based on close status
        if followup.close_status in ['Win', 'Loss']:
            return redirect('my_work')
        return redirect('follow_up_4', lead_id=lead_id)

    return render(request, 'follow_up_3.html', {
        'lead': lead,
        'sales_persons': sales_persons,
    })


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

#close lead function
@login_required
def closed_leads(request):
    closed = Lead.objects.filter(is_closed=True, follow_up_person=request.user)
    return render(request, 'close_lead.html', {'closed_leads': closed})


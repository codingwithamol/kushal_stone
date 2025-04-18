from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Sales', 'Sales'),
        ('Operations', 'Operations'),
        ('Manager', 'Manager'),
        ('Finance', 'Finance')
    ]
    
    mobile_number = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    # Add related_name to prevent clash
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',  # Unique reverse relation for CustomUser
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Unique reverse relation for CustomUser
        blank=True
    )
    
    # class Meta:
    #     unique_together = ('mobile_number', 'role')  # Ensure unique combination of mobile_number and role


class Product(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name




from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Lead(models.Model):
    CUSTOMER_SEGMENT_CHOICES = [
        ('Retail/individual', 'Retail/individual'),
        ('B2B', 'B2B'),
        ('Reseller', 'Reseller'),
        ('Commercial/Corporate', 'Commercial/Corporate')
    ]

    SOURCE_CHOICES = [
        ('Instagram', 'Instagram'),
        ('Facebook', 'Facebook'),
        ('Indiamart', 'Indiamart'),
        ('Google', 'Google'),
        ('Reference', 'Reference'),
        ('Other', 'Other')
    ]

    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField()
    requirements = models.CharField(max_length=50)
    products = models.ManyToManyField('Product', blank=True)
    services = models.ManyToManyField('Service', blank=True)
    address = models.TextField()
    architect_name = models.CharField(max_length=100)
    architect_number = models.CharField(max_length=15)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    source_other = models.CharField(max_length=100, blank=True, null=True)
    enquiry_date = models.DateField()
    sales_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='sales_person')
    customer_segment = models.CharField(max_length=50, choices=CUSTOMER_SEGMENT_CHOICES)
    next_followup_date = models.DateField(null=True, blank=True)
    follow_up_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='follow_up_person')
    is_closed = models.BooleanField(default=False)
    win_status = models.BooleanField(null=True, blank=True)  
    closed_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='closed_leads')

    # assigned_to = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_leads')


    def __str__(self):
        return self.full_name
    
from django.utils import timezone


class FollowUpBase(models.Model):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)

    LEAD_TYPE_CHOICES = [
        ('Hot', 'Hot'),
        ('Warm', 'Warm'),
        ('Cold', 'Cold'),
        ('Not Interested', 'Not Interested')
    ]

    followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    lead_type = models.CharField(max_length=20, choices=LEAD_TYPE_CHOICES)
    remarks = models.TextField()
    close_status = models.CharField(
        max_length=10,
        choices=[('Open', 'Open'), ('Win', 'Win'), ('Loss', 'Loss')],
        default='Open',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        abstract = True

class FollowUp1(FollowUpBase):
    lead = models.OneToOneField(Lead, on_delete=models.CASCADE)
    customer_visited = models.BooleanField()
    inspection_done = models.BooleanField()
    quotation_given = models.BooleanField()
    quotation_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    quotation_file = models.FileField(upload_to='quotations/', null=True, blank=True)
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup2_person')


class FollowUp2(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup3_person')

class FollowUp3(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup4_person')


class FollowUp4(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup5_person')


class FollowUp5(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup6_person')


class FollowUp6(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup7_person')


class FollowUp7(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup8_person')


class FollowUp8(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup9_person')


class FollowUp9(FollowUpBase):
    next_followup_date = models.DateField(null=True, blank=True)
    next_followup_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='followup10_person')


class FollowUp10(FollowUpBase):
    # No next follow-up
    pass

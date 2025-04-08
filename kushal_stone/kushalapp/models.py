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
    products = models.ManyToManyField(Product, blank=True)
    services = models.ManyToManyField(Service, blank=True)
    address = models.TextField()
    architect_name = models.CharField(max_length=100)
    architect_number = models.CharField(max_length=15)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES)
    source_other = models.CharField(max_length=100, blank=True, null=True)
    enquiry_date = models.DateField()
    sales_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='sales_person')
    customer_segment = models.CharField(max_length=50, choices=CUSTOMER_SEGMENT_CHOICES)
    follow_up_date = models.DateField()
    follow_up_person = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='follow_up_person')

    def __str__(self):
        return self.full_name
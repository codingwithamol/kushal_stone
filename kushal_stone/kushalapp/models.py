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
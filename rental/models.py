import datetime 
import uuid

from django.core.validators import MaxValueValidator
from django.db import models
from django.urls.base import reverse

from accounts.models import CustomUser

from django.utils import timezone

from django.utils.translation import gettext_lazy as _


class Manufacturer(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name 


class CarModel(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, null=True, verbose_name="model")

    def __str__(self):
        #str() is a temporary addition to solve admin CarModel page error (For some reason, self.name returns 'None') on the main page alone. 
        return str(self.name) 

    
class Insurance(models.Model):
    provider = models.CharField(max_length=100, help_text="Current insurance provider", verbose_name="Insurance Provider", blank=True)
    
    COVERAGE_TYPE = (
        ('c', 'Comprehensive'),
        ('t', 'Third Party'),
        ('n', 'None'),
    )

    coverage = models.CharField(
        max_length=1,
        choices=COVERAGE_TYPE,
        blank=True,
        default='c',
        help_text='Insurance coverage type'
    )

    def __str__(self):
        return self.provider

    class Meta:
        verbose_name = _("insurance provider")
        verbose_name_plural = _("insurance providers")
    

# Change the name of this model to "category". 
class Category(models.Model):
    """Model representing class of car. (Saloon, Estate, Pickup, Medium 4x4, Large 4x4 etc...)"""

    CATEGORY_CHOICES = (
        ('sm','Saloon/Estate'),
        ('md','Medium 4x4'),
        ('lg','Large 4x4'),
        ('sf', 'Safari'),
        ('pu','Pickup'),
        ('xl','Bus/Van'),
    )

    name = models.CharField(
        max_length=2,
        choices=CATEGORY_CHOICES,
        blank=True,
        default='sm'
    )

    def __str__(self):
        return self.get_name_display()

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
    

class Car(models.Model):
    """Model representing individual car in database."""
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    # Model year. Validator ensures that no model year  can be set in the future. 
    year = models.IntegerField(validators=[MaxValueValidator(int(datetime.date.today().year) + 1)], null=True, default=2022)
    engine_size = models.IntegerField(default=2500, help_text="Engine size in cc (e.g. 2500, 1600)")
    license_plate = models.CharField(max_length=8, default="KBD 001A")
    color = models.CharField(max_length=50, blank=True, null=True, default='White')
    owner = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="owner")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    
    SEATING_OPTIONS = (
        ('5', 'Five'),
        ('7', 'Seven'),
        ('8', 'Eight'),
        ('9', 'Nine'),
        ('8', 'Eight'),
        ('25', 'Twenty-Five'),
    )

    seats = models.CharField(choices=SEATING_OPTIONS, max_length=2, blank=True)

    FUEL_OPTIONS = (
        ('p', 'Petrol'),
        ('d', 'Diesel'),
    )

    fuel = models.CharField(
        max_length=1,
        choices=FUEL_OPTIONS,
        blank=True,
        default='p',
    )

    DRIVETRAIN_OPTIONS = (
        ('AWD', 'All Wheel Drive'),
        ('FWD', 'Front Wheel Drive'),
        ('RWD', 'Rear Wheel Drive'),
    )

    drivetrain = models.CharField(
        max_length=4,
        choices = DRIVETRAIN_OPTIONS,
        blank=True,
        default='RWD',
    )

    TRANSMISSION_OPTIONS = (
        ('AT', 'Automatic'),
        ('MT', 'Manual'),
    )
        
    transmission = models.CharField(
        max_length=4,
        choices=TRANSMISSION_OPTIONS,
        blank=True,
        default='AT'
    )

    STATUS_CHOICES = (
        ('a', 'Available'),
        ('r', 'Reserved'),
        ('h', 'On Hire'),
        ('m', 'Maintenance'),
    )

    status = models.CharField(
        max_length=1,
        choices = STATUS_CHOICES,
        default='a',
    )

    # Fields for individual car in database
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Automatically generated unique ID. Do not change.")
    mileage = models.IntegerField(null=True)
    
    insurance = models.ForeignKey(Insurance, on_delete=models.RESTRICT, null=True, verbose_name='current insurance provider')
    insurance_expiry_date = models.DateField(null=True, blank=True)

    daily_rate = models.IntegerField(default=3500, help_text="Daily rate in Kenyan Shillings")

    def __str__(self):
        return f'{ self.manufacturer } { self.model }'

    @property
    def insurance_expired(self):
        """Determines if insurance is expired based on due date and current date."""
        return bool(self.insurance_expiry_date and datetime.date.today() > self.insurance_expiry_date)

    class Meta:
        ordering = []
        permissions = (("can_change_availability", "Set car as rented"),)

    def get_absolute_url(self):
        return reverse('rental:car-detail', args=[str(self.id)])

    def __unicode__(self):
        return f'{ self.manufacturer } { self.model }'
        

# Rename to 'hire' to better distinguish between booking, hiring, and invoicing.
class Booking(models.Model):
    """Stores the bookings, for example when it was made, the booking date, and the car ID."""

    # Unique ID for this booking.
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Automatically generated unique ID. Do not change.")
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True)

    delivery = models.BooleanField(blank=True, null=True)
    chauffer_driven = models.BooleanField(blank=True, null=True)
    
    STATUS_CHOICES = (
        ('p', 'Pending'),
        ('i', 'In Progress'),
        ('c', 'Complete'),
    )

    booking_status = models.CharField(choices=STATUS_CHOICES, default='i', max_length=1)

    @property
    def get_total_days(self):
        """Subtracts start_date from end_date and returns the # days as integer."""
        return (self.end_date - self.start_date).days

    @property
    def get_total_cost(self):
        """Calculates total cost of order by multiplying total days by daily rate of car."""
        total = 0
        days = self.get_total_days

        total = self.get_total_days * self.car.daily_rate

        
        if self.chauffer_driven == True:
            total += (2000 * days)

        if self.delivery == True:
            total += 1,000
        
        return total

    def __str__(self):
        return f'{ self.created_by } | { self.car } | ( {self.start_date} - { self.end_date })'

    def get_absolute_url(self):
        return reverse('rental:booking-detail', args=[str(self.id)])

class Invoice(models.Model):
    id = id = models.AutoField(primary_key=True)

    STATUS_CHOICES = (
        ('p', 'Pending'),
        ('c', 'Cleared'),
        ('e', 'Expired'),
        ('s', 'Success'),
    )

    created = models.DateTimeField(default=timezone.now, blank=True)
    due = models.DateField(blank=True)
    
    status = models.CharField(choices=STATUS_CHOICES, max_length=1, blank=True)


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.SET_NULL, null=True)



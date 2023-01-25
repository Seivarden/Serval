from django.contrib import admin
from .models import  Manufacturer, Category, CarModel, Car, Insurance, Booking, Invoice, Payment

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display= ('manufacturer', 'model')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    display_name = 'Categories'

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_filter = ['manufacturer', 'owner']
    sortable_by = ['manufacturer', 'year']

    list_display = ('manufacturer', 'model', 'license_plate', 'owner', 'status')
    fieldsets = (
        (None, {
            'fields': ('manufacturer', 'model', 'year', 'color', 'engine_size', 'fuel', 'drivetrain', 'transmission', 'mileage')
        }) ,
        ('Category', {
            'fields': ('category', 'seats')
        }) ,
        ('Legal', {
            'fields': ('owner', 'insurance', 'insurance_expiry_date', 'license_plate')
        }),

        ('Rental', {
            'fields': ('daily_rate', 'status')
        })
    )

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    pass

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'created_by', 'start_date', 'end_date', 'booking_status')
    sortable_by = ['end_date', 'start_date', 'car']

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass

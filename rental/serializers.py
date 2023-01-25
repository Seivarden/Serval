from rest_framework import serializers
from .models import Car, Booking
from accounts.models import CustomUser

class CarSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='rental:car-detail', format='html')

    class Meta:
        model = Car
        fields = ['url', 'id', 'manufacturer', 'model', 'owner', 'color', 'year']

class BookingSerializer(serializers.ModelSerializer):
    client = serializers.ReadOnlyField(source='client.first_name')

    class Meta: 
        model = Booking
        fields = ['id', 'car', 'start_date', 'client', 'end_date']

class UserSerializer(serializers.ModelSerializer):
    cars = serializers.PrimaryKeyRelatedField(many=True, queryset=Car.objects.all())
    # customer_id = serializers.ReadOnlyField(source='Customer.id')
    # customer_url = serializers.HyperlinkedIdentityField(
    #     view_name='customer-detail',
    #     source='customer_id',
    #     lookup_field='pk',
    #     )
    user = serializers.ReadOnlyField(source='CustomUser.user')

    class Meta: 
        model = CustomUser
        fields = ['user', 'bookings', 'cars']


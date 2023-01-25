import datetime

from rest_framework import generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView 
from accounts.models import CustomUser
from .models import Booking, Car
from .serializers import BookingSerializer, CarSerializer, UserSerializer

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView

from django.shortcuts import render, get_object_or_404

from . import forms

from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly 


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'cars': reverse('car-list', request=request, format=format),
    })    


class IndexView(APIView):
    """Website homepage. Currently simple, only showing number of Cars and Customers in database."""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'index.html'

    def get(self, request):    
        num_cars = Car.objects.all().count()
        num_users = CustomUser.objects.all().count()
        num_bookings = Booking.objects.all().count()

        return Response({
            'num_cars': num_cars,
            'num_users': num_users,
            'num_bookings': num_bookings,
        })


class CarListView(generics.ListCreateAPIView):
    """Displays all the cars in the database"""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'car-list.html'

    def get(self, request):
        car_list = Car.objects.all()
        serializer_class = CarSerializer

        return Response({
            'car_list': car_list,
        })


class CarDetailView(DetailView):
    """Displays all information about a specific car."""
    model = Car
    template_name = 'car-detail.html'


class BookingListView(generics.ListCreateAPIView):
    """Showcases all the bookings in the system."""
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'booking-list.html'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        booking_list = Booking.objects.all()
        serializer_class = BookingSerializer

        return Response({
            'booking_list': booking_list,
        })


class BookingDetailView(DetailView):
    """Information about a specific booking made in the system."""
    model = Booking
    template_name = 'booking-detail.html'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


permission_classes = [permissions.IsAuthenticated]
class BookingCreate(CreateView):
    model = Booking
    fields = ['car', 'start_date', 'end_date']


    def form_valid(self, form):
        form.instance.created_by = CustomUser.objects.get(pk=self.request.user.pk)
        # form.instance.created_by = self.request.user
        # form.instance.created_by = Booking.objects.get(created_by=self.request.user).user
        return super().form_valid(form)


class BookingUpdate(UpdateView):
    model = Booking
    fields = ['start_date', 'end_date']


class UserListView(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'user-list.html'

    def get(self, request):
        queryset = CustomUser.objects.all()
        serializer_class = UserSerializer

        return Response({
            'customer_list': queryset,
        })

    def perform_create(self, serializer):
        serializer.save(client=self.request.user)
        

class UserDetailView(DetailView):
    model = CustomUser
    template_name = 'user-detail.html'

    """
    # form.instance.user = self.request.user
    # form.instance.user = Booking.objects.get(user=self.request.user)
    # form.instance.user = Booking.objects.get(user=self.request.user).user 
    # form.instance.user=get_object_or_404(Booking,user=self.request.user).user 
    """

class GeneralListView(ListView):
    model = Car
    template_name = 'cars_by_category.html'

    def get_queryset(self):
        return Car.objects.filter(category__name='sm').filter(status='a')

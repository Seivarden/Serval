from django.contrib import admin
from django.urls import path, include
import rest_framework
from django.views.generic import RedirectView

import rest_registration

from accounts.views import customers, owners 

urlpatterns = [
    path('', RedirectView.as_view(url='rentals', permanent=True)),
    path('admin/', admin.site.urls),
    path('rentals/', include('rental.urls')),
    path('accounts/', include('rest_registration.api.urls')),
    path('accounts/signup/customer', customers.CustomerSignUpView.as_view(), name='customer_signup'),
    path('accounts/signup/customer', owners.OwnerSignUpView.as_view(), name='owner_signup'),
]

import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from . import models


# class PlaceOrderForm(forms.Form):
#     """Initial order forms for customers."""
#     start_date = forms.DateField(help_text='When do you want the car?')
#     end_date = forms.DateField(help_text='When will you return the car?')

#     def clean_data(self, date):
#         data = self.cleaned_data(date)

#         # Check that start date is not in the past
#         if data < datetime.date.today():
#             raise ValidationError(_('Invalid date: Start in past.'))

#         # Ensure that start date is not today (to avoid last_minute bookings.)
#         if data == datetime.date.today():
#             raise ValidationError(_('Invalid date: Please reserve your car at least 24 hours in advance.'))

#         return data

#     cleaned_start_date = clean_data(start_date)
#     cleaned_end_date = clean_data(end_date)
    
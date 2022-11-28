from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext_lazy
from django.utils import timezone
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

User = get_user_model()
#RegisteredUser Model
class Profile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True) #Should be OnetoOne. I don't think it's possible for a User to have more than one profile ~ Victoria Bedar
    Name = models.CharField(max_length = 100)
    Points = models.PositiveIntegerField(default=0)
    DinerNum = models.PositiveIntegerField(null = True)
    PaymentMethod = models.CharField(max_length = 50, null = True)
    #Address Details M stands for "Mail"
    MstAddress = models.CharField(max_length = 100)
    MCity = models.CharField(max_length = 100)
    MState = models.CharField(max_length = 40)
    MZip = models.CharField(max_length = 9)
    # B stands for "Billing"
    BstAddress = models.CharField(max_length = 100)
    BCity = models.CharField(max_length = 100)
    BState = models.CharField(max_length = 40)
    BZip = models.CharField(max_length = 9)
    Phone_validator = RegexValidator(regex=r'^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$', message="Please enter a valid Phone Number")
    pPhone = models.CharField(validators=[Phone_validator], max_length=17, null = True)
    pEmail = models.EmailField(max_length=100, null = True)

#Table Model
class Table (models.Model):
    Capacity = models.PositiveIntegerField(default=2)
    isReserved = models.BooleanField(default=False)
    def __str__(self):
        return 'Table ' + str(self.id) + ' (Seats ' + str(self.Capacity) + ')'

#Reservation Model
def date_validator (ResDate):
    if ResDate < timezone.now():
        raise ValidationError("You cannot book a table in the past")


class Reservation (models.Model):
    Name = models.CharField(max_length=100)
    Phone_validator = RegexValidator(regex=r'^(\([0-9]{3}\) |[0-9]{3}-)[0-9]{3}-[0-9]{4}$', message="Please enter a valid Phone Number")
    Phone = models.CharField(validators=[Phone_validator],max_length=17)
    Email = models.EmailField(max_length=100)
    Time = models.DateTimeField(validators=[date_validator])
    GuestNum = models.PositiveIntegerField()
    isHighTraffic = models.BooleanField(default=False)
    # def limitQuery(self):
    #      q = Reservation.objects.filter(Time__gte = self.Time)
    #      for Table in q.iterator():
    #          #T = Table.objects.get(pk=q.Table.id)
    #          #T.isReserved = True
    #          Table.isReserved = True
    #      return 
    Table = models.ForeignKey(Table, on_delete = models.CASCADE, limit_choices_to={'isReserved':False}, null=True)
    #When trying to add this field it says that the 1st parameter needs to be a model even though that's exactly what I did (the parameters are literally the same as Table) ~ Victoria Bedar
    #Table2 = models.ForeignKey(Table, on_delete = models.CASCADE, limit_choices_to={'isReserved':False}, null=True)

class dateWidget(forms.widgets.DateTimeInput):
    input_type = 'datetime-local'

class ReservationForm (ModelForm):
    class Meta:
        model = Reservation
        exclude = ['Phone_validator','HoldFee', 'Table', 'isHighTraffic']
        labels = {
            'Time':gettext_lazy('Reservation Time'),
            'GuestNum':gettext_lazy('Party of'),
            'Phone':gettext_lazy('Phone (in format ###-###-#### or (###) ###-####)')
        } 
        widgets = {
            'Time':dateWidget()
        }

class RTableForm (ModelForm):
    class Meta:
        model = Reservation
        fields = ['Table']

class HighTrafficDay(models.Model):
    date = models.DateTimeField(validators=[date_validator])
    name = models.CharField(max_length=100)
    #Christmas - 12/25
    #Christmas Eve - 12/24
    #Thanksgivng - 4th Thursday of November
    #Good Friday - Varies by year (2023-04-07, 2024-03-29, 2025-04-18)
    #Labor Day - 1st Monday of September
    #New Years Day - 01/01
    #New Years Eve - 12/31
    #4th of July - 07/04
    #Memorial Day - Last Monday of May
    #Veterans Day - 11/11
    #MLK - 3rd Monday of January
    #Halloween - 10/31

# List of name, date pairs of high traffic days.
High_Traffic_Days = [
    ('Christmas', datetime(2021, 12, 25)),
    ('Christmas Eve', datetime(2021, 12, 24)),
    ('Thanksgiving', datetime(2021, 11, 25)),
    ('Good Friday', datetime(2021, 4, 2)),
    ('Labor Day', datetime(2021, 9, 6)),
    ('New Years Day', datetime(2021, 1, 1)),
    ('New Years Eve', datetime(2021, 12, 31)),
    ('4th of July', datetime(2021, 7, 4)),
    ('Memorial Day', datetime(2021, 5, 31)),
    ('Veterans Day', datetime(2021, 11, 11)),
    ('MLK', datetime(2021, 1, 18)),
    ('Halloween', datetime(2021, 10, 31)),
]





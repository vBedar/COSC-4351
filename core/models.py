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

# Create your models here.
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
    #HoldFee = models.DecimalField(max_digits=100, decimal_places=2, null=True) #For high traffic days. Thinking of tracking those by marking true if it's a holiday, weekend, or if a ceratin amount of tables are reserved ~ Victoria Bedar
    isHighTraffic = models.BooleanField(default=False)
    isRegistered = models.BooleanField(default=False)
    # def limitQuery(self):
    #      q = Reservation.objects.filter(Time__gte = self.Time)
    #      for Table in q.iterator():
    #          #T = Table.objects.get(pk=q.Table.id)
    #          #T.isReserved = True
    #          Table.isReserved = True
    #      return 
    Table = models.ForeignKey(Table, on_delete = models.CASCADE, limit_choices_to={'isReserved':False}, null=True)

class dateWidget(forms.widgets.DateTimeInput):
    input_type = 'datetime-local'

class ReservationForm (ModelForm):
    class Meta:
        model = Reservation
        exclude = ['Phone_validator','HoldFee', 'Table', 'isHighTraffic', 'isRegistered']
        labels = {
            'Time':gettext_lazy('Reservation Time'),
            'GuestNum':gettext_lazy('Party of'),
            'Phone':gettext_lazy('Phone (in format ###-###-#### or (###) ###-####)')
        } 
        widgets = {
            'Time':dateWidget()
        }
        #Supposed to get table capacity > guestNum validation working but it's not ~ Victoria Bedar
        # def clean(self):
        #     cleaned_data = super().clean()
        #     GuestNum = cleaned_data.get("GuestNum")
        #     Table = cleaned_data.get("Table")
        #      #if gN and T:
        #     if GuestNum > Table.Capacity:
        #     raise ValidationError("Table can not accommodate amount of guests")
class RTableForm (ModelForm):
    class Meta:
        model = Reservation
        fields = ['Table']

class HighTrafficDay(models.Model):
    date = models.DateTimeField(validators=[date_validator])
    name = models.CharField(max_length=100)

# Create your models here.

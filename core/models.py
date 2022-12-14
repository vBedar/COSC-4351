from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model
import uuid
import datetime
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

    def __str__(self):
        return 'Name: ' + str(self.Name) + ' Email: ' + str(self.pEmail) + ' Phone: ' + str(self.pPhone)  + ' Points: ' + str(self.Points) + ' Diner Number: ' + str(self.DinerNum) + ' Perferred Payment Method: ' + str(self.PaymentMethod) + ' Mailing address: ' + str(self.MstAddress) + ' ' + str(self.MCity) + ', ' + str(self.MState) + ' ' + str(self.MZip) + ' Billing Address: ' + str(self.BstAddress)  + ' ' + str(self.BCity) + ', ' + str(self.BState) + ' ' + str(self.BZip)

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
    Table = models.ForeignKey('Table', on_delete = models.CASCADE, limit_choices_to={'isReserved':False}, null=True)
    TableT = models.ForeignKey('Table', on_delete = models.CASCADE, limit_choices_to={'isReserved':False}, null=True, related_name='TableT', blank=True)
    
    def __str__(self):
        return str(self.Name) + ' ' + str(self.Phone) + ' ' + str(self.Email) + ' ' + str(self.Time) + ' Guest: ' + str(self.GuestNum) + ' Table: ' + str(self.Table) + ' Table2: ' + str(self.TableT)

    def clean(self):
        if self.Table == self.TableT and self.Table is not None:
            raise ValidationError("You cannot combine the same table")

class dateWidget(forms.widgets.DateTimeInput):
    input_type = 'datetime-local'

class ReservationForm (ModelForm):
    class Meta:
        model = Reservation
        exclude = ['Phone_validator','HoldFee', 'Table','TableT', 'isHighTraffic']
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
        fields = ['Table', 'TableT']

# Tracks high traffic days that may change year to year.
class HighTrafficDay(models.Model):
    date = models.DateTimeField(validators=[date_validator])
    name = models.CharField(max_length=100)


# List of (Month, Day) tuples for holidays (fixed dates).
Holidays = [
    (1, 1), # New Years Day
    (12, 31), # New Years Eve
    (7, 4), # 4th of July
    (11, 11), # Veterans Day
    (12, 25), # Christmas
    (12, 24), # Christmas Eve
    (10, 31), # Halloween
    (5, 31), # Memorial Day
    (1, 31), # MLK
    (9, 1), # Labor Day
    (11, 4), # Thanksgiving
    (4, 7), # Good Friday
    (2, 14), # Valentines Day
]





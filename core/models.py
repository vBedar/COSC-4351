from distutils.command.upload import upload
from email.policy import default
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
from django.forms import ModelForm
from django.utils.translation import gettext_lazy

# Create your models here.
User = get_user_model()
#RegisteredUser Model
class RegisteredUser (models.Model):
    User = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True, default=None)
    Name = models.CharField(max_length = 100)
    Points = models.PositiveIntegerField()
    DinerNum = models.PositiveIntegerField(null = True)
    PaymentMethod = models.CharField(max_length = 50, null = True)
    #Address Details M stands for "Mail"
    MstAddress1 = models.CharField(max_length = 100)
    MstAddress2 = models.CharField(max_length = 100, blank=True, null=True)
    MCity = models.CharField(max_length = 100)
    STATES = [
        ('AL', 'Alabama'),
        ('AK', 'Alaska'),
        ('AZ', 'Arizona'),
        ('AR', 'Arkansas'),
        ('CA', 'California'),
        ('CO', 'Colorado'),
        ('CT', 'Connecticut'),
        ('DE', 'Delaware'),
        ('FL', 'Florida'),
        ('GA', 'Georgia'),
        ('HI', 'Hawaii'),
        ('ID', 'Idaho'),
        ('IL', 'Illinois'),
        ('IN', 'Indiana'),
        ('IA', 'Iowa'),
        ('KS', 'Kansas'),
        ('KY', 'Kentucky'),
        ('LA', 'Louisiana'),
        ('ME', 'Maine'),
        ('MD', 'Maryland'),
        ('MA', 'Massachusetts'),
        ('MI', 'Michigan'),
        ('MN', 'Minnesota'),
        ('MS', 'Mississippi'),
        ('MO', 'Missouri'),
        ('MT', 'Montana'),
        ('NE', 'Nebraska'),
        ('NV', 'Nevada'),
        ('NH', 'New Hamphire'),
        ('NJ', 'New Jersey'),
        ('NM', 'New Mexico'),
        ('NY', 'New York'),
        ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('OH', 'Ohio'),
        ('OK', 'Oklahoma'), 
        ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('RI', 'Rhode Island'),
        ('SC', 'South Carolina'),
        ('SD', 'South Dakota'),
        ('TN', 'Tennessee'),
        ('TX', 'Texas'),
        ('UT', 'Utah'),
        ('VT', 'Vermont'),
        ('VA', 'Virginia'),
        ('WA', 'Washington'),
        ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'),
        ('WY', 'Wyoming'), 
    ]
    MState = models.CharField(max_length = 2, choices=STATES)
    MZip = models.CharField(max_length = 9)
    BillingIsMailing = models.BooleanField()
    # B stands for "Billing"
    BstAddress1 = models.CharField(max_length = 100)
    BstAddress2 = models.CharField(max_length = 100, blank=True, null=True)
    BCity = models.CharField(max_length = 100)
    BState = models.CharField(max_length = 2, choices=STATES)
    BZip = models.CharField(max_length = 9)

    def get_billing_address(self):
        if self.BillingIsMailing:
            self.BstAddress1 = self.MstAddress1
            self.BstAddress2 = self.MstAddress2
            self.BCity = self.MCity
            self.BState = self.MState
            self.BZip = self.BZip

class UserForm(ModelForm):
    class Meta:
        model = RegisteredUser
        #I'd like to make it to where the Billing Address stuff only shows up when the checkbox isn't checked. Not sure how that's done with ModelForms rn but will check. Push comes to shove I'll just auto fill the fields when the box is checked ~ Victoria Bedar
        fields = ['Name', 'MstAddress1', 'MstAddress2', 'MState', 'MCity', 'MZip', 'BillingIsMailing', 'BstAddress1', 'BstAddress2', 'BState', 'BCity', 'BZip']
        labels = {
            'Name': gettext_lazy('Enter Your Name'),
            'MstAddress1':gettext_lazy('Enter Your Mailing Address'),
            'MstAddress2':gettext_lazy('Enter Your Secondary Mailing Address (optional)'),
            'MState':gettext_lazy('Choose Your State'),
            'MCity':gettext_lazy('Enter Your City'),
            'MZip':gettext_lazy('Enter Your ZipCode'),
            'BillingIsMailing':gettext_lazy('Is Your Billing Address The Same As Your Mailing Address?'),
            'BstAddress1':gettext_lazy('Enter Your Billing Address'),
            'BstAddress2':gettext_lazy('Enter Your Secondary Billing Address (optional)'),
            'BState':gettext_lazy('Choose Your State'),
            'BCity':gettext_lazy('Enter Your City'),
            'BZip':gettext_lazy('Enter Your ZipCode'),    
        }
# Create your models here.

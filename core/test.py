from django.test import TestCase
from core.models import User, Profile, Reservation, ReservationForm, Table, HighTrafficDay
import datetime
from django.utils import timezone

# Create your tests here.
class ReservationTest(TestCase):
    def test_Phone_Validation_valid(self):
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        #Valid Phones
        VResForm1 = ReservationForm(data={'Name':'James', 'Phone':'123-456-7890', 'Email':'j@j.com', 'Time':date, 'GuestNum':3})
        VResForm2 = ReservationForm(data={'Name':'James', 'Phone':'(123) 456-7890', 'Email':'j@j.com', 'Time':date, 'GuestNum':3})

        self.assertTrue(VResForm1.is_valid())
        self.assertTrue(VResForm2.is_valid())

    def test_Phone_Validation_invalid(self):
        date = datetime.datetime.now() + datetime.timedelta(days=1)

        #Invalid Phones
        IResForm1 = ReservationForm(data={'Name':'James', 'Phone':'123-456-789', 'Email':'j@j.com', 'Time':date, 'GuestNum':3})
        IResForm2 = ReservationForm(data={'Name':'James', 'Phone':'123-46-7890', 'Email':'j@j.com', 'Time':date, 'GuestNum':3})
        IResForm3 = ReservationForm(data={'Name':'James', 'Phone':'1234567890', 'Email':'j@j.com', 'Time':date, 'GuestNum':3})
        IResForm4 = ReservationForm(data={'Name':'James', 'Phone':'12-345-67890', 'Email':'j@j.com', 'Time':date, 'GuestNum':3})
        IResForm5 = ReservationForm(data={'Name':'James', 'Phone':'(123 456-7890', 'Email':'j@j.com', 'Time':date, 'GuestNum':3})
        IResForm6 = ReservationForm(data={'Name':'James', 'Phone':'123) 456-7890', 'Email':'j@j.com', 'Time':date, 'GuestNum':3})
        IResForm7 = ReservationForm(data={'Name':'James', 'Phone':'12', 'Email':'j@j.com', 'Time':date, 'GuestNum':3})
        IResForm8 = ReservationForm(data={'Name':'James', 'Phone':'abc-def-ghij', 'Email':'j@j.com', 'Time':date, 'GuestNum':3})

        self.assertFalse(IResForm1.is_valid())
        self.assertFalse(IResForm2.is_valid())
        self.assertFalse(IResForm3.is_valid())
        self.assertFalse(IResForm4.is_valid())
        self.assertFalse(IResForm5.is_valid())
        self.assertFalse(IResForm6.is_valid())
        self.assertFalse(IResForm7.is_valid())
        self.assertFalse(IResForm8.is_valid())
    
    def test_Date_validation(self):
        validDate = datetime.datetime.now() + datetime.timedelta(days=1)
        invalidDate = datetime.datetime.now() - datetime.timedelta(days=1)

        vForm = ReservationForm(data={'Name':'James', 'Phone':'123-456-7890', 'Email':'j@j.com', 'Time':validDate, 'GuestNum':3})
        iForm = ReservationForm(data={'Name':'James', 'Phone':'123-456-7890', 'Email':'j@j.com', 'Time':invalidDate, 'GuestNum':3})

        self.assertTrue(vForm.is_valid())
        self.assertFalse(iForm.is_valid())

class ViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u1 = User.objects.create_user(username='Felix', password='1234')
        u1.save()
    def test_profile_view_nologin(self):
        response1 = self.client.get('profile')
        self.assertEqual(response1.status_code, 404)
    #Trying to test that page can be accessed if logged in. Test doesn't seem to be working ~ Victoria Bedar
    # def test_login_req_profile(self):
    #     login = self.client.login(username='Felix', password='1234')
    #     response1 = self.client.get('profile')

    #     self.assertEqual(str(response1.context['user']), 'u1')
    #     self.assertEqual(response1.status_code, 200)
    #     self.assertTemplateUsed(response1, 'profile.html')
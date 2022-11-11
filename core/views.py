
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Profile
# Create your views here.

@login_required(login_url='signin')
def index(request):
    user_object = User.objects.get(username=request.user.username)
    return render(request, 'index.html')


def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                # log user in and redirect to setting page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile obejct for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('/')

        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')

    else:
        return render(request, 'signup.html')

def signin(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def profile(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile,
    }

    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def setting(request):

    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        name = request.POST['Name']
        #dinerNum = request.POST['DinerNum'] #Shouldn't be in the form these are system generated ~ Victoria Bedar
        payment = request.POST['Payment']
        shippingAd = request.POST['ShippingAd']
        shipCity = request.POST['ShipCity']
        shipZipCode = request.POST['ShipZipCode']
        shipstates = request.POST['states']
        billingAd = request.POST['BillingAd']
        billCity = request.POST['BillCity']
        billZipcode = request.POST['BillZipCode']
        billstates = request.POST['states2']
        user_profile.Name = name
        #user_profile.DinerNum = dinerNum
        user_profile.PaymentMethod = payment
        user_profile.MstAddress = shippingAd
        user_profile.MCity = shipCity
        user_profile.MState = shipstates
        user_profile.MZip = shipZipCode

        user_profile.BstAddress = billingAd
        user_profile.BCity = billCity
        user_profile.BState = billstates
        user_profile.BZip = billZipcode
        user_profile.save()

        return redirect('profile')


    return render(request, 'setting.html', {'user_profile': user_profile} )

# Class based view documentation:
# https://docs.djangoproject.com/en/4.1/topics/class-based-views/intro/
class reservationPage(TemplateView):
    '''Display reservation parameters to user, 
        Calculate table(s) required to accommodate,
        Reserve table(s) for guest'''
    template_name = "reservation.html"
    context = {}
    def get(self, request): # Function called for GET request        
        return render(request, 'reservation.html')
    
    def post(self, request): # Called for POST requests        
        return render(request, 'reservation.html')

    def table_allocation(num_guests):
        '''Find and allocate available tables to seat num_guests.'''
        # return [list_of_table_id's] ?
        pass
   


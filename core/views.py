
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from .models import Profile, Reservation, Table, ReservationForm
# Create your views here.

#@login_required(login_url='signin')
def index(request):    
    #user_object = User.objects.get(username=request.user.username)
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
    return redirect('index')

@login_required(login_url='signin')
def profile(request):
    if Profile.objects.filter(user = request.user).exists():
        user_profile = Profile.objects.get(user=request.user)
    else:
        return redirect('setting')
    context = {
        'user_profile': user_profile,
    }

    return render(request, 'profile.html', context)


@login_required(login_url='signin')
def setting(request):

    #user_profile = Profile.objects.get(user=request.user)
    if Profile.objects.filter(user = request.user).exists():
        user_profile = Profile.objects.get(user=request.user)
        #Not sure how to auto-fill without using Django forms but we should do it if the User has a profile and also have the user's email filled~ Victoria Bedar
    else:
        user_profile = Profile(user=request.user)
    if request.method == 'POST':
        name = request.POST['Name']
        #dinerNum = request.POST['DinerNum'] #Shouldn't be in the form these are system generated ~ Victoria Bedar
        payment = request.POST['Payment']
        shippingAd = request.POST['ShippingAd']
        shipCity = request.POST['ShipCity']
        shipZipCode = request.POST['ShipZipCode']
        shipstates = request.POST['states']
        Pphone = request.POST.get('phoneEntry', None)
        Pemail = request.POST.get('emailEntry', None)
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
        user_profile.pPhone = Pphone
        user_profile.pEmail = Pemail

        user_profile.BstAddress = billingAd
        user_profile.BCity = billCity
        user_profile.BState = billstates
        user_profile.BZip = billZipcode
        user_profile.save()

        return redirect('profile')


    return render(request, 'setting.html')#, {'user_profile': user_profile} )

# Class based view documentation:
# https://docs.djangoproject.com/en/4.1/topics/class-based-views/intro/
class reservationPage(TemplateView):
    '''Display reservation parameters to user, 
        Calculate table(s) required to accommodate,
        Reserve table(s) for guest'''
    template_name = "reservation.html"
    #context = {}
    #user_obj = get_object_or_404(User, pk=1)

    def get(self, request): # Function called for GET request
        if Profile.objects.filter(user = request.user).exists():
            user_profile = Profile.objects.get(user = request.user)
            data = {'Name':user_profile.Name, 'Phone':user_profile.pPhone, 'Email':user_profile.pEmail, 'Time':"", 'GuestNum':""}
            form = ReservationForm(initial=data)
        else:
            form = ReservationForm()        
        # User data to populate initial form fields.
        context = {"form": form}
        # if(request.user.is_authenticated):
        #     user_profile = Profile.objects.filter(user=request.user)[0]
        #     context['Name'] = user_profile.Name
        #     #context['Name'] = user_profile.
                               
        return render(request, 'reservation.html', context)
    
    def post(self, request): # Called for POST requests 
        reservation = Reservation()#user=user_obj)
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation.Name = form.cleaned_data['Name']
            reservation.Phone = form.cleaned_data['Phone']
            reservation.Email = form.cleaned_data['Email']
            reservation.Time = form.cleaned_data['Time']
            reservation.GuestNum = form.cleaned_data['GuestNum']
            reservation.save()
            return HttpResponse('Form Submitted')
        return render(request, 'reservation.html', {'form':form})

    #def table_allocation(num_guests):
        #'''Find and allocate available tables to seat num_guests.'''
        # return [list_of_table_id's] ?
        #if Table.objects.filter(isReserved = False).count() == 0:
            #messages.info(request, 'No tables avalible')
            #return redirect('reservationPage')
        #if Table.objects.filter(isReserved = False, Capacity >= Current_Reservation.GuestNum).count() > 0:
            #Display table list: Table.objects.filter(isReserved = False, Capacity >= Current_Reservation)
            #Set whatever table object is chosen isReserved value to True
            #Redirect to confirmation page or display confirmation message
        #else:
            #The Table combining method will go here
        #pass
   



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from datetime import timedelta
import random
from .models import Profile, Reservation, Table, ReservationForm, RTableForm, HighTrafficDay, Holidays
# Create your views here.

#@login_required(login_url='signin')
def index(request):    
    #user_object = User.objects.get(username=request.user.username)
    #resetting tables for limit_choices_to ~ Victoria Bedar
    for t in Table.objects.all():
        t.isReserved = False
        t.save()  
    #For those that quit half-way through the reservation process by hitting Home~ Victoria Bedar    
    Reservation.objects.filter(Table=None).delete()
    Tables = Table.objects.all()
    if(Tables.count() < 5):
        # Populate the table database.
        for i in range(10):
            Table.objects.create(Capacity = random.randint(2,8),isReserved=False)
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
                new_profile.pEmail = email
                random.seed(user_model.id, 2)
                new_profile.DinerNum=random.randrange(1000000, 10000000)
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
        messages.info(request, 'Profile Updated Successfully.')
        return redirect('profile')


    return render(request, 'setting.html', {'user_profile': user_profile} )

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
        # This is needed for auto-filling ~ Victoria Bedar
        if(request.user.is_authenticated):
            user_profile = Profile.objects.get(user = request.user)
            # User data to populate initial form fields.
            data = {'Name':user_profile.Name, 'Phone':user_profile.pPhone, 'Email':user_profile.pEmail, 'Time':"", 'GuestNum':""}
            form = ReservationForm(initial=data)
        else:
            form = ReservationForm()  
        context = {"form": form}
                               
        return render(request, 'reservation.html', context)
    
    def post(self, request): # Called for POST requests 
        #print("POST request received")
        reservation = Reservation()
        if(request.user.is_authenticated):
            reservation.isRegistered = True
        form = ReservationForm(request.POST)
        if form.is_valid():
            #print("Form is valid")
            reservation.Name = form.cleaned_data['Name']
            reservation.Phone = form.cleaned_data['Phone']
            reservation.Email = form.cleaned_data['Email']
            reservation.Time = form.cleaned_data['Time']
            reservation.GuestNum = form.cleaned_data['GuestNum']
            # Check if date is in high traffic days list or on a weekend.
            #print("Date: ", reservation.Time.date())
            #print("Weekday(): ", reservation.Time.weekday())
                # TODO: Prompt for holding fee, ask for card info if not on file for user.
            print("Reservation.Time.date: ", reservation.Time.date())            
            if(self.isHighTraffic(reservation.Time.date())):
                reservation.isHighTraffic = True
            # else:
            #     print("Low traffic day reservation.")
            
            reservation.save()
            return redirect('/reservation/%d'%reservation.id)
            # reservation.Table = form.cleaned_data['Table']
            """ 
            Rough Validation for preventing guests from reserving a table
            with lower capacity. Would rather get something like this 
            working in the models/forms if possible ~ Victoria Bedar
            """
            # if reservation.GuestNum > reservation.Table.Capacity:
            #     return render(request, 'reservation.html', {'form':form})
            # else:
            #     reservation.save()
            #     return HttpResponse('Form Submitted')
        return render(request, 'reservation.html', {'form':form})

    """
    def table_allocation(num_guests):
        '''Find and allocate available tables to seat num_guests.'''
        return [list_of_table_id's] ?
        if Table.objects.filter(isReserved = False).count() == 0:
            messages.info(request, 'No tables avalible')
            return redirect('reservationPage')
        if Table.objects.filter(isReserved = False, Capacity >= Current_Reservation.GuestNum).count() > 0:
            Display table list: Table.objects.filter(isReserved = False, Capacity >= Current_Reservation)
            Set whatever table object is chosen isReserved value to True
            Redirect to confirmation page or display confirmation message
        else:
            The Table combining method will go here
        pass
    """
    
    '''Check if date is in high traffic days list or on a weekend.'''
    def isHighTraffic(reservationObj, date):
        # print("reservationObj:", reservationObj)
        # print("date: ", date)
        monthDay = (date.month, date.day)
        if(monthDay in Holidays):
            return True
        if(date.weekday() >= 4):
            return True
        #TODO: Query HighTrafficDays table for date.
        htd = HighTrafficDay.objects.filter(date=date)
        if(htd):
            return True
        #TODO: Check if limited seating left on this date.
        r = Reservation.objects.filter(Time=date)
        if(r.count() >= 30):
            return True
        return False
   
"""
Determine which tables are unavailable through other reservations. 
Tables where isReserved = False are displayed to the user in the 
RTableForm because of the lmit_choices_to attribute in the Table
model.
"""
def reserveTable(request, r_id):
    reservation = Reservation.objects.get(pk=r_id)
    TableCombine=False
    ValidComboExists = False
    optimalTables = []
    if reservation.isHighTraffic:
        messages.info(request, "We're expecting a lot of traffic today. If you continue with your reservation, you'll be charged with a hold fee.")
    #Set choice limit using Query (I would have limit_choices_to be limited by a function that calls self but that doesn't work) ~ Victoria Bedar
    resQuery = Reservation.objects.filter(Time__gte = reservation.Time - timedelta(hours=1)).filter(Time__lte = reservation.Time + timedelta(hours=1))
    for otherRes in resQuery: # Iterate through Reservations within 1 hour of current reservation.
        # Set the tables of those reservations to unavailable.
        if Table.objects.filter(pk=otherRes.Table_id).exists():
            T=Table.objects.get(pk=otherRes.Table_id)
            T.isReserved = True
            T.save()
        if Table.objects.filter(pk=otherRes.TableT_id).exists():
            TT=Table.objects.get(pk=otherRes.TableT_id)
            TT.isReserved = True
            TT.save()    
    # Check if there are any tables left available for the reservation.
    if Table.objects.filter(isReserved=False).count() <= 0:
        messages.warning(request, 'No Tables Avalible, Reservation Aborted. Please Click the Home Button and Try Again')
        reservation.delete()
    # If only 1 table available, check if it can seat the reservation.
    elif Table.objects.filter(isReserved=False).count() == 1:
        t1 = Table.objects.get(isReserved=False)
        if t1.Capacity < reservation.GuestNum:
            messages.warning(request, 'No Tables Avalible, Reservation Aborted. Please Click the Home Button and Try Again')
            reservation.delete()
    
    else: # Multiple tables available.
        freeTables = Table.objects.filter(isReserved=False).order_by('Capacity')
        # List of tables that belong to optimal table group.                
        
        # print("\n\nNum guests: ", reservation.GuestNum)
        # print("Tables available for reservation.")
        for t in freeTables: # Iterate through available tables smallest first to find best fit.                        
            #print("t: ", t)
            if(t.Capacity >= reservation.GuestNum): # Smallest table that can seat reservation.
                optimalTables.append(t)
                break

        # No single table can seat reservation. Add largest table to optimalTables.
        if len(optimalTables) == 0:
            optimalTables.append(freeTables.last())
            TableCombine=True
                    
        #print("First optimal table: ", optimalTables[0])
        # If second table required iterate through remaining tables again.
        if(TableCombine):           
            for t in freeTables:
                # Skip table already selected.
                if(t in optimalTables):
                    continue
                # If second table found, add to optimalTables.
                if(optimalTables[0].Capacity + t.Capacity >= reservation.GuestNum):
                    t.isReserved = True
                    t.save()
                    optimalTables.append(t)
                    ValidComboExists = True
                    break
            
            #print("optimalTables: ", optimalTables)
            
            if ValidComboExists:        
                messages.warning(request, 'Table combining needed')                    
            else:
                messages.warning(request, 'No Tables Avalible, Reservation Aborted. Please Click the Home Button and Try Again')
        
    # Set all tables to unavailable except for optimalTables.
    for t in Table.objects.all():
        if(t not in optimalTables):
            #print("\nt NOT IN: ", t)
            #print("opt_tables: ", optimalTables)
            t.isReserved = True
            t.save()
        else:
            #print("\nt IN: ", t)
            t.isReserved = False
            t.save()            
            

    if request.method == 'POST':
        form = RTableForm(request.POST)
        if form.is_valid():
            reservation.Table = form.cleaned_data['Table']
            reservation.TableT = form.cleaned_data['TableT']
            if reservation.Table is not None and reservation.TableT is not None:
                T1 = Table.objects.get(pk=reservation.Table_id)
                T2 = Table.objects.get(pk=reservation.TableT_id)
                if T1.Capacity + T2.Capacity < reservation.GuestNum:
                    messages.error(request, 'Insufficient Capacity. Please choose a different combination')   
                else:
                    reservation.save()           
                    return redirect('/reservation/%d/confirmation'%r_id)
            else:
                if TableCombine and reservation.TableT is None:
                    messages.error(request,'A second Table is needed')
                else:
                    reservation.save()           
                    return redirect('/reservation/%d/confirmation'%r_id)               
    else:
        form = RTableForm()
    context = {
        'form':form,
        'TableCombine':TableCombine,
    }
    return render(request, 'TReservation.html', context)


def confirmation(request, r_id):
    reservation = Reservation.objects.get(pk=r_id)
    for t in Table.objects.all():
         t.isReserved = False
         t.save()      
    return render(request, 'confirmation.html', {'reservation':reservation})
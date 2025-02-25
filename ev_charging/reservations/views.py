from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import  Station, Reservation, Slot
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import send_reservation_email
from django.utils import timezone
import datetime

def home(request):
    return render(request, 'home.html')


# Login View
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('reservation')  # ✅ Redirect to reservation page
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

# Signup View
def signup_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()  # ✅ Save user
            login(request, user)  # ✅ Automatically log in new user
            return redirect('reservation')  # ✅ Redirect to reservations.html
    else:
        form = SignUpForm()
    
    return render(request, "signup.html", {"form": form})

# Reservation View
@login_required
def reservation(request):
    stations = Station.objects.all()
    slots = Slot.objects.filter(is_available=True)

    if request.method == 'POST':
        slot_id = request.POST.get('slot')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if not slot_id or not start_time or not end_time:
            messages.error(request, "⚠ All fields are required!")
            return redirect('reservation')

        slot = get_object_or_404(Slot, id=slot_id)

        # ✅ Prevent double booking
        if not slot.is_available:
            messages.error(request, "⚠ This slot is already booked! Please choose another slot.")
            return redirect('reservation')

        # ✅ Convert string input to timezone-aware datetime
        start_time = timezone.make_aware(datetime.datetime.fromisoformat(start_time))
        end_time = timezone.make_aware(datetime.datetime.fromisoformat(end_time))

        # ✅ Mark the slot as unavailable
        slot.is_available = False
        slot.save()

        # ✅ Create reservation
        reservation = Reservation.objects.create(
            user=request.user,
            slot=slot,
            start_time=start_time,
            end_time=end_time
        )

        # ✅ Send confirmation email
        subject = "EV Charging Reservation Confirmed 🚗⚡"
        message = f"""
        Hi {request.user.username},

        Your EV charging slot has been successfully reserved!

        📍 Station: {reservation.slot.station.name}
        🔢 Slot Number: {reservation.slot.slot_number}
        ⏰ Start Time: {reservation.start_time}
        ⏳ End Time: {reservation.end_time}

        Thank you for using our service!

        Regards,  
        EV Charging Team
        """
        send_reservation_email(request.user.email, subject, message)

        messages.success(request, "✅ Reservation successful! A confirmation email has been sent.")
        return redirect('reservation_success', reservation.id)

    return render(request, 'reservation.html', {'stations': stations, 'slots': slots})
@login_required
def reservation_success(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'reservation_success.html', {'reservation': reservation})

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'my_reservations.html', {'reservations': reservations})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)

    # ✅ Mark slot as available again
    reservation.slot.is_available = True
    reservation.slot.save()

    reservation.delete()

    # ✅ Send cancellation email
    subject = "EV Charging Reservation Canceled ❌"
    message = f"""
    Hi {request.user.username},

    Your EV charging reservation has been **canceled**.

    📍 Station: {reservation.slot.station.name}
    🔢 Slot Number: {reservation.slot.slot_number}

    If this was a mistake, feel free to book again.

    Regards,  
    EV Charging Team
    """
    send_reservation_email(request.user.email, subject, message)

    messages.success(request, "Your reservation has been canceled. A confirmation email has been sent.")
    return redirect('my_reservations')

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
import qrcode
from io import BytesIO
import base64
from .models import Station
from .models import Announcement
from reservations.ml_models.demand_model import predict_demand
from reservations.ml_models.demand_model import add_reservation_to_csv

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

    # ✅ Show only slots that are available OR whose last reservation has ended
    current_time = timezone.now()
    slots = Slot.objects.filter(
        is_available=True
    ) | Slot.objects.filter(
        reservation__end_time__lt=current_time  # Show slots where the last reservation has ended
    )

    if request.method == 'POST':
        slot_id = request.POST.get('slot')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        carpool = request.POST.get('carpool') == "on"  # ✅ Check if carpooling is selected

        if not slot_id or not start_time or not end_time:
            messages.error(request, "⚠ All fields are required!")
            return redirect('reservation')

        slot = get_object_or_404(Slot, id=slot_id)

        # ✅ Convert string input to timezone-aware datetime
        start_time = timezone.make_aware(datetime.datetime.fromisoformat(start_time))
        end_time = timezone.make_aware(datetime.datetime.fromisoformat(end_time))

        # ✅ Validate that start_time is in the future
        if start_time < timezone.now():
            messages.error(request, "⚠ Start time must be in the future!")
            return redirect('reservation')

        # ✅ Validate that end_time is after start_time
        if end_time <= start_time:
            messages.error(request, "⚠ End time must be after start time!")
            return redirect('reservation')

        # ✅ Check if the slot is already booked during the requested time
        overlapping_reservations = Reservation.objects.filter(
            slot=slot,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if overlapping_reservations:
            messages.error(request, "⚠ This slot is already booked for the selected time!")
            return redirect('reservation')

        # ✅ Create reservation with carpooling preference
        reservation = Reservation.objects.create(
            user=request.user,
            slot=slot,
            start_time=start_time,
            end_time=end_time,
            carpool_opt_in=carpool  # ✅ Save carpooling choice
        )

        # ✅ Find carpooling users (same station & overlapping time)
        carpool_matches = Reservation.objects.filter(
            slot__station=reservation.slot.station,  # Same station
            start_time__lt=reservation.end_time,  # Overlapping time
            end_time__gt=reservation.start_time,  # Overlapping time
            carpool_opt_in=True  # Must have opted for carpooling
        ).exclude(user=reservation.user)  # Exclude current user

        # ✅ Send reservation data to AI model
        add_reservation_to_csv(slot.station.id, start_time.weekday(), start_time.hour)

        # ✅ Send confirmation email
        subject = "EV Charging Reservation Confirmed 🚗⚡"
        message = f"""
        Hi {request.user.username},

        Your EV charging slot has been successfully reserved!

        📍 Station: {reservation.slot.station.name}
        🔢 Slot Number: {reservation.slot.slot_number}
        ⏰ Start Time: {reservation.start_time}
        ⏳ End Time: {reservation.end_time}

        { "🚗 You have opted for carpooling! Here are your carpool matches:\n" if carpool_matches else "If you want to carpool, you can edit your reservation." }
        { ''.join([f'- {match.user.username}\n' for match in carpool_matches]) if carpool_matches else '' }

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

    # Generate QR code
    qr_data = f"Reservation ID: {reservation.id}\nStation: {reservation.slot.station.name}\nSlot: {reservation.slot.slot_number}\nStart: {reservation.start_time}\nEnd: {reservation.end_time}"
    qr = qrcode.make(qr_data)
    
    # Convert QR code to base64 for embedding in HTML
    qr_buffer = BytesIO()
    qr.save(qr_buffer, format="PNG")
    qr_base64 = base64.b64encode(qr_buffer.getvalue()).decode()

    return render(request, 'reservation_success.html', {'reservation': reservation, 'qr_code': qr_base64})

@login_required
def my_reservations(request):
    """Show all reservations for the logged-in user and fetch potential carpool users."""

    # ✅ Fetch all reservations for the current user
    user_reservations = Reservation.objects.filter(user=request.user)

    # ✅ Fetch ALL reservations where carpooling is enabled, in the same station, and has overlapping time
    all_carpool_reservations = Reservation.objects.filter(
        slot__station__in=user_reservations.values_list('slot__station', flat=True),  # Same station
        carpool_opt_in=True
    ).exclude(user=request.user)  # ✅ Exclude the current user

    return render(request, 'my_reservations.html', {
        'reservations': user_reservations,  # ✅ User's own reservations
        'all_carpool_reservations': all_carpool_reservations  # ✅ Carpool matches
    })  

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

def station_map(request):
    stations = Station.objects.all()
    return render(request, 'stations.html', {'stations': stations})

def dummy_payment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    # ✅ Simulate a successful payment
    reservation.is_paid = True  
    reservation.save()

    messages.success(request, "✅ Payment Successful! Your slot is confirmed.")
    return redirect("my_reservations")  # Redirect back to reservations

def announcements(request):
    all_announcements = Announcement.objects.order_by('-created_at')  # Latest first
    return render(request, 'announcements.html', {'announcements': all_announcements})
def recommend_slot(request):
    station_id = int(request.GET.get("station_id"))
    day = int(request.GET.get("day"))
    hour = int(request.GET.get("hour"))

    prediction = predict_demand(station_id, day, hour)
    
    return JsonResponse({"recommended_demand": prediction})
from django.db import models
from django.contrib.auth.models import User
import qrcode
import base64
from io import BytesIO

class Station(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    total_slots = models.IntegerField()
    def __str__(self):
        return f"{self.name} - {self.location}" 

class Slot(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    slot_number = models.IntegerField()
    is_available = models.BooleanField(default=True)

class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
    carpool_opt_in = models.BooleanField(default=False)
    qr_code = models.TextField(blank=True, null=True)  # ✅ Add QR Code field

    def generate_qr_code(self):
        """Generate a QR code for the reservation."""
        qr = qrcode.make(f"Reservation ID: {self.id}\nUser: {self.user.username}\nStation: {self.slot.station.name}")
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    def save(self, *args, **kwargs):
        # ✅ Generate QR Code if it does not exist
        if not self.qr_code:
            qr = qrcode.make(f"Reservation ID: {self.id}\nUser: {self.user.username}\nStation: {self.slot.station.name}")
            buffer = BytesIO()
            qr.save(buffer, format="PNG")
            self.qr_code = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        super().save(*args, **kwargs)

class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
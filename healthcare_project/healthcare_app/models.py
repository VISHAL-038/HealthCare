from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from decimal import Decimal


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')


# Doctor Profile
class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, default="General")
    experience = models.IntegerField(null=True, blank=True)  # Allow NULL values
    contact_number = models.CharField(max_length=15, default="N/A")


# Patient Profile
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    contact_number = models.CharField(max_length=15)


# Prediction History
class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.TextField()
    predicted_disease = models.CharField(max_length=255)
    prediction_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.predicted_disease} ({self.prediction_date})"


# Appointment
User = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_appointments")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_appointments")
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Appointment with Dr. {self.doctor.username} on {self.date} at {self.time}"


class Prescription(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_prescriptions")
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_prescriptions")
    diagnosis = models.TextField()
    prescribed_medicines = models.TextField()
    additional_notes = models.TextField(blank=True, null=True)
    date_issued = models.DateTimeField(default=now)

    def __str__(self):
        return f"Prescription for {self.patient.username} by Dr. {self.doctor.username}"


class PatientReport(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    report_name = models.CharField(max_length=255)
    report_pdf = models.FileField(upload_to="reports/pdfs/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.report_name} - {self.patient.username}"


# ✅ Fixed Patient History (Added created_at)
class PatientHistory(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE)  # One-to-One Relationship
    medical_conditions = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    medications = models.TextField(blank=True, null=True)
    surgeries = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)  # ✅ Add timestamp for history creation

    def __str__(self):
        return f"Medical History of {self.patient.username}"
    

class Medicine(models.Model):
    generic_name = models.CharField(max_length=255)
    brand_names = models.CharField(max_length=255)
    typical_use = models.TextField()
    price_range = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    image_link = models.URLField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.generic_name} ({self.brand_names})"

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.quantity * self.medicine.price  

    def __str__(self):
        return f"{self.user.username} - {self.medicine.generic_name} ({self.quantity})"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), null=False, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    order_date = models.DateTimeField(default=now)

    def __str__(self):
        return f"Order {self.id} - {self.user.username} ({self.medicine.generic_name})"
    
# raiting
class Testimonial(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.rating}⭐"

# availabe test 
class AvailableLabTest(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name

class LabTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(AvailableLabTest, on_delete=models.CASCADE)
    test_date = models.DateField()
    test_time = models.TimeField()

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return f"{self.user.username} - {self.test.name}"

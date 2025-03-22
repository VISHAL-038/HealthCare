from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, DoctorProfile, PatientProfile, Appointment, Prescription, PatientReport, PatientHistory, Testimonial,  AvailableLabTest, LabTest

# Custom User Registration Form
class UserRegisterForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

# Doctor Profile Form
class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['specialization', 'experience', 'contact_number']

# Patient Profile Form
class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['age', 'gender', 'contact_number']

# symptom forms
class SymptomForm(forms.Form):
    symptoms = forms.CharField(
        label="Enter Symptoms (comma-separated)",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g., fever, cough, headache"})
    )

# appoipment
class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=User.objects.filter(user_type="doctor"), empty_label="Select a Doctor")

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time', 'reason']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

# preciption
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'diagnosis', 'prescribed_medicines', 'additional_notes']
        widgets = {
            'prescribed_medicines': forms.Textarea(attrs={'rows': 3}),
            'additional_notes': forms.Textarea(attrs={'rows': 3}),
        }

# Reports
class PatientReportForm(forms.ModelForm):
    class Meta:
        model = PatientReport
        fields = ["report_name", "report_pdf"]

class PatientHistoryForm(forms.ModelForm):
    class Meta:
        model = PatientHistory
        fields = ["medical_conditions", "allergies", "medications", "surgeries"]
        widgets = {
            "medical_conditions": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter past medical conditions"}),
            "allergies": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter any allergies"}),
            "medications": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter ongoing medications"}),
            "surgeries": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Enter past surgeries (if any)"}),
        }

# raitings
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['feedback', 'rating']
        widgets = {
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Share your experience...'}),
            'rating': forms.Select(attrs={'class': 'form-control'}, choices=[(i, f"{i} Stars") for i in range(1, 6)])
        }

# lab test
class LabTestForm(forms.ModelForm):
    test = forms.ModelChoiceField(
        queryset=AvailableLabTest.objects.all(),
        empty_label="Select a test",
        label="Lab Test"
    )

    class Meta:
        model = LabTest
        fields = ["test", "test_date", "test_time"]
        widgets = {
            "test_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "test_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
        }

class HealthPredictionForm(forms.Form):
    age = forms.IntegerField(min_value=18, max_value=100, label="Age")
    bmi = forms.FloatField(min_value=10.0, max_value=50.0, label="BMI")
    blood_pressure = forms.IntegerField(min_value=80, max_value=200, label="Blood Pressure")
    heart_rate = forms.IntegerField(min_value=40, max_value=150, label="Heart Rate")
    blood_sugar = forms.IntegerField(min_value=50, max_value=600, label="Blood Sugar")
    cholesterol = forms.IntegerField(min_value=100, max_value=400, label="Cholesterol")
